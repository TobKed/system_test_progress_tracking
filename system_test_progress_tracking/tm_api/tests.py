from django.test import TestCase
from faker import Faker
from rest_framework.test import APITestCase


class DryRunViewTest(APITestCase):
    def setUp(self):
        fake = Faker()
        self.test_data_dict = {
            "machine_name": fake.name(),
            "timestamp": fake.date_time(),
            "master_scenario": {
                "file_name": fake.file_name(extension="py"),
                "file_path": "/".join(fake.file_path(depth=10).split("/")[:-1]),
                "script": fake.text(),
                "scenarios": [
                    {
                        "file_name": fake.file_name(extension="py"),
                        "file_path": "/".join(fake.file_path(depth=10).split("/")[:-1]),
                        "script": fake.text(),
                    },
                    {
                        "file_name": fake.file_name(extension="py"),
                        "file_path": "/".join(fake.file_path(depth=10).split("/")[:-1]),
                        "script": fake.text(),
                    },
                ]
            }
        }

    def test_post_dry_run(self):
        response = self.client.post("/tm_api/dry_run/", data=self.test_data_dict, format='json')
        print(response.content)
        self.assertEqual(response.status_code, 201)
