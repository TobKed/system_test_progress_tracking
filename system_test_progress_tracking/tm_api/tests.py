import random
from django.test import TestCase
from faker import Faker
from django.db import IntegrityError
from rest_framework.test import APITestCase
from .models import BaseScript, TEST_STATUS_CHOICES


fake = Faker()


def get_random_status():
    return random.choice(TEST_STATUS_CHOICES)[1]


def setUpModule():
    print("setUpModule")


def tearDownModule():
    print("tearDownModule")


class BaseScriptModelTest(TestCase):
    def create_base_script(
            self,
            file_name=fake.file_name(extension="py"),
            file_path="/".join(fake.file_path(depth=10).split("/")[:-1]),
            script=fake.text(),
            _status=get_random_status(),
            timestamp_start=fake.date_time(),
            timestamp_stop=fake.date_time()):
        return BaseScript.objects.create(
            file_name=file_name,
            file_path=file_path,
            script=script,
            _status=_status,
            timestamp_start=timestamp_start,
            timestamp_stop=timestamp_stop)

    def test_base_script_creation(self):
        b = self.create_base_script()
        self.assertTrue(isinstance(b, BaseScript))
        self.assertEqual(b.__str__(), b.file_name)

    def test_base_script_status_property(self):
        b = self.create_base_script()
        self.assertEqual(b._status, b.status)
        b.status = "running"
        self.assertEqual(b._status, "running")
        b.status = get_random_status()
        self.assertEqual(b._status, b.status)
        with self.assertRaises(IntegrityError):
            b.status = "wrong status"


#TODO
class TestModelTest(TestCase):
    pass


#TODO
class ScenarioModelTest(TestCase):
    pass


#TODO
class MasterScenarioModelTest(TestCase):
    pass


#TODO
class DryRunData(TestCase):
    pass


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
                        "tests": [
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

                        ],
                    },
                    {
                        "file_name": fake.file_name(extension="py"),
                        "file_path": "/".join(fake.file_path(depth=10).split("/")[:-1]),
                        "script": fake.text(),
                        "tests": [
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
                        ],
                    },
                ]
            }
        }

    def test_post_dry_run(self):
        response = self.client.post("/tm_api/dry_run/", data=self.test_data_dict, format='json')
        print(response.content)
        self.assertEqual(response.status_code, 201)
