from django.test import TestCase
from django.db import IntegrityError
from rest_framework.test import APITestCase
from tm_api.models import (
    Machine,
    BaseScript,
)

from . import random_properties
from . import db_operations


def setUpModule():
    print("setUpModule")


def tearDownModule():
    print("tearDownModule")


class BaseScriptModelTest(TestCase):
    def test_base_script_creation(self):
        b = db_operations.create_base_script()
        self.assertTrue(isinstance(b, BaseScript))
        self.assertEqual(b.__str__(), b.file_name)

    def test_base_script_status_property(self):
        b = db_operations.create_base_script()
        self.assertEqual(b._status, b.status)
        b.status = "running"
        self.assertEqual(b._status, "running")
        b.status = random_properties.get_random_status()
        self.assertEqual(b._status, b.status)
        with self.assertRaises(IntegrityError):
            b.status = "wrong status"


class MachineModelTest(TestCase):
    def test_machine_test_creation(self):
        m = db_operations.create_machine()
        self.assertTrue(isinstance(m, Machine))
        self.assertEqual(m.__str__(), m.machine_name)


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
            "machine_name": random_properties.get_random_machine_name(),
            "timestamp": random_properties.get_random_time_stamp(),
            "master_scenario": {
                "file_name": random_properties.get_random_file_name(),
                "file_path": random_properties.get_random_file_path(),
                "script": random_properties.get_random_script(),
                "scenarios": [
                    {
                        "file_name": random_properties.get_random_file_name(),
                        "file_path": random_properties.get_random_file_path(),
                        "script": random_properties.get_random_script(),
                        "tests": [
                            {
                                "file_name": random_properties.get_random_file_name(),
                                "file_path": random_properties.get_random_file_path(),
                                "script": random_properties.get_random_script(),
                            },
                            {
                                "file_name": random_properties.get_random_file_name(),
                                "file_path": random_properties.get_random_file_path(),
                                "script": random_properties.get_random_script(),
                            },

                        ],
                    },
                    {
                        "file_name": random_properties.get_random_file_name(),
                        "file_path": random_properties.get_random_file_path(),
                        "script": random_properties.get_random_script(),
                        "tests": [
                            {
                                "file_name": random_properties.get_random_file_name(),
                                "file_path": random_properties.get_random_file_path(),
                                "script": random_properties.get_random_script(),
                            },
                            {
                                "file_name": random_properties.get_random_file_name(),
                                "file_path": random_properties.get_random_file_path(),
                                "script": random_properties.get_random_script(),
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
