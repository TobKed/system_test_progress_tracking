import random
from django.test import TestCase
from faker import Faker
from django.db import IntegrityError
from rest_framework.test import APITestCase
from tm_api.models import (
    BaseScript,
    Test,
    Scenario,
    MasterScenario,
    DryRunData,
    Machine,
    TEST_STATUS_CHOICES,
)

from .random_properties import (
    get_random_machine_name,
    get_random_status,
    get_random_file_name,
    get_random_file_path,
    get_random_script,
    get_random_time_stamp,
)


def setUpModule():
    print("setUpModule")


def tearDownModule():
    print("tearDownModule")


class BaseScriptModelTest(TestCase):
    def create_base_script(
            self,
            file_name=get_random_file_name(),
            file_path=get_random_file_path(),
            script=get_random_script(),
            _status=get_random_status(),
            timestamp_start=get_random_time_stamp(),
            timestamp_stop=get_random_time_stamp()):
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
class DryRunDataModelTest(TestCase):
    pass


class DryRunViewTest(APITestCase):
    def setUp(self):
        self.test_data_dict = {
            "machine_name": get_random_machine_name(),
            "timestamp": get_random_time_stamp(),
            "master_scenario": {
                "file_name": get_random_file_name(),
                "file_path": get_random_file_path(),
                "script": get_random_script(),
                "scenarios": [
                    {
                        "file_name": get_random_file_name(),
                        "file_path": get_random_file_path(),
                        "script": get_random_script(),
                        "tests": [
                            {
                                "file_name": get_random_file_name(),
                                "file_path": get_random_file_path(),
                                "script": get_random_script(),
                            },
                            {
                                "file_name": get_random_file_name(),
                                "file_path": get_random_file_path(),
                                "script": get_random_script(),
                            },

                        ],
                    },
                    {
                        "file_name": get_random_file_name(),
                        "file_path": get_random_file_path(),
                        "script": get_random_script(),
                        "tests": [
                            {
                                "file_name": get_random_file_name(),
                                "file_path": get_random_file_path(),
                                "script": get_random_script(),
                            },
                            {
                                "file_name": get_random_file_name(),
                                "file_path": get_random_file_path(),
                                "script": get_random_script(),
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
