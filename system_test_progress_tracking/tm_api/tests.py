from django.test import TestCase
from faker import Faker
from rest_framework.test import APITestCase
import json


class DryRunViewTest(APITestCase):
    def setUp(self):
        fake = Faker()
        self.test_data_dict = {
            "machine_name": fake.name(),
            "time_stamp": fake.date_time(),
            "master_scenario": {
                # "file_name": "scenario_master.py",
                "file_name": fake.file_name(extension="py"),
                "file_path": "/".join(fake.file_path(depth=10).split("/")[:-1]),
                "script": "import os\nfrom run import SCENARIOS_DIR, run_test_scenario\n\n\nrun_test_scenario(os.path.join(SCENARIOS_DIR, \"scenario_01_feature_lamp.py\"))\nrun_test_scenario(os.path.join(SCENARIOS_DIR, \"scenario_02_feature_door.py\"))\nrun_test_scenario(os.path.join(SCENARIOS_DIR, \"scenario_03_feature_trunk.py\"))\n"
            }
        }

    def test_post_dry_run(self):
        response = self.client.post("/tm_api/dry_run/", data=self.test_data_dict, format='json')
        print(response.content)
        self.assertEqual(response.status_code, 201)
