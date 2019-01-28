from django.urls import reverse
from rest_framework import status
from django.test import TestCase
from django.db import IntegrityError
from rest_framework.test import APITestCase
from tm_api.models import (
    Machine,
    BaseScript,
    MasterScenario,
    Scenario,
    Test,
    DryRunData
)

from . import random_properties
from . import db_operations


def setUpModule():
    print("set up tm_api.tests")
    db_operations.populate_db()


def test_basic_status_set(test_obj, instance):
    test_obj.assertEqual(instance._status, instance.status)
    instance.status = "running"
    test_obj.assertEqual(instance._status, "running")
    instance.status = random_properties.get_random_status()
    test_obj.assertEqual(instance._status, instance.status)
    with test_obj.assertRaises(IntegrityError):
        instance.status = "wrong status"


class BaseScriptModelTest(TestCase):
    def test_base_script_creation(self):
        b = db_operations.create_base_script()
        self.assertTrue(isinstance(b, BaseScript))
        self.assertEqual(b.__str__(), b.file_name)

    def test_base_script_status_property(self):
        b = db_operations.create_base_script()
        test_basic_status_set(self, b)


class MachineModelTest(TestCase):
    def test_machine_test_creation(self):
        m = db_operations.create_machine()
        self.assertTrue(isinstance(m, Machine))
        self.assertEqual(m.__str__(), m.machine_name)


class MasterScenarioModelTest(TestCase):
    def test_master_scenario_creation(self):
        ms = db_operations.create_master_scenario()
        self.assertTrue(isinstance(ms, MasterScenario))
        self.assertEqual(ms.__str__(), ms.file_name)
        
    def test_master_scenario_status_property(self):
        ms = db_operations.create_master_scenario()
        test_basic_status_set(self, ms)

    def test_tests_status(self):
        ms = db_operations.get_random_obj(MasterScenario)
        self.assertTrue(ms.tests_status)


class ScenarioModelTest(TestCase):
    def test_scenario_creation(self):
        s = db_operations.create_scenario()
        self.assertTrue(isinstance(s, Scenario))
        self.assertEqual(s.__str__(), s.file_name)

    def test_test_status_property(self):
        s = db_operations.create_scenario()
        #FIXME
        with self.assertRaises(AttributeError):
            s.status = "passed"


class TestModelTest(TestCase):
    def test_test_creation(self):
        t = db_operations.create_test()
        self.assertTrue(isinstance(t, Test))
        self.assertEqual(t.__str__(), t.file_name)

    def test_test_status_property(self):
        t = db_operations.create_test()
        test_basic_status_set(self, t)


class DryRunDataModelTest(TestCase):
    def test_dry_run_data_creation(self):
        machine = db_operations.get_random_obj(Machine)
        timestamp = random_properties.get_random_time_stamp()
        master_scenario = db_operations.create_master_scenario()
        dr = db_operations.create_dry_run_data(machine=machine, timestamp=timestamp, master_scenario=master_scenario)
        self.assertTrue(isinstance(dr, DryRunData))
        self.assertEqual(dr.__str__(), f"DryRunData: {machine.machine_name} - {timestamp}")


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
        dry_run_count_before = DryRunData.objects.count()
        master_scenario_count_before = MasterScenario.objects.count()
        scenario_count_before = Scenario.objects.count()
        test_count_before = Test.objects.count()
        url = reverse('tm_api:dry-run-input')
        data = self.test_data_dict
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        dry_run_count_diff = DryRunData.objects.count() - dry_run_count_before
        master_scenario_count_diff = MasterScenario.objects.count() - master_scenario_count_before
        scenario_count_diff = Scenario.objects.count() - scenario_count_before
        test_count_diff = Test.objects.count() - test_count_before
        self.assertEqual(dry_run_count_diff, 1)
        self.assertEqual(master_scenario_count_diff, 1)
        self.assertEqual(scenario_count_diff, 2)
        self.assertEqual(test_count_diff, 4)
