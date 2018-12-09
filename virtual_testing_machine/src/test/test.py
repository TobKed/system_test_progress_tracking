import unittest
import os
from time import time
from unittest.mock import MagicMock
import run
import test_runner.actions
import test_runner.models


class TestDirsFiles(unittest.TestCase):
    def test_dirs(self):
        self.assertTrue(os.path.isdir(run.BASE_DIR))
        self.assertTrue(os.path.isdir(run.TEST_CASES_DIR))
        self.assertTrue(os.path.isdir(run.SCENARIOS_DIR))

    def test_files(self):
        self.assertTrue(os.path.exists(run.SCENARIO_MASTER))


class TestRunTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_case_path = os.path.join(run.TEST_CASES_DIR, "01_feature_lamp", "01_01_test_lamp.py")

    def test_test_case_path(self):
        self.assertTrue(os.path.exists(self.test_case_path))

    def test_run_test_case(self):
        time_start = time()
        test_runner.actions.run_test_case(self.test_case_path)
        time_end = time()
        execution_time = time_end - time_start
        self.assertTrue(1.5 < execution_time < 2.5)

    @unittest.mock.patch("test_runner.actions.run_script")
    def test_runners(self, mocked_run_script):
        test_path = run.SCENARIO_MASTER
        test_runner.actions.run_test_case(test_path)
        test_runner.actions.run_test_scenario(test_path)
        test_runner.actions.run_scenario_master(test_path)
        self.assertEqual(
            mocked_run_script.call_args_list,
            [
                unittest.mock.call(test_path, "test_case"),
                unittest.mock.call(test_path, "scenario"),
                unittest.mock.call(test_path, "master"),
            ]
        )
        self.assertEqual(mocked_run_script.call_count, 3)


class TestRunDataTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.script_data_dict = {
            "file_path": "test\\path",
            "file_name": "test file name",
            "script": "import os",
        }
        cls.scenario_data_dict = {**cls.script_data_dict, **{"tests": None}}
        cls.master_scenario_data_dict = {**cls.script_data_dict, **{"scenarios": None}}

    def test_RunData_object(self):
        run_data = test_runner.models.RunData()
        self.assertFalse(run_data._dry_run_active)
        self.assertIsNone(run_data.dry_run_data)
        self.assertFalse(run_data.is_running)
        run_data.dry_run = True
        self.assertTrue(isinstance(run_data.dry_run_data, test_runner.models.DryRunData))

    def test_ScriptData_object(self):
        with self.assertRaises(Exception):
            test_runner.models.ScriptData()

        script_data = test_runner.models.ScriptData(**self.script_data_dict)
        self.assertIs(script_data.__str__(), script_data.file_name)
        self.assertEqual(script_data.convert_to_dict(), self.script_data_dict)
        
    def test_TestCase_object(self):
        with self.assertRaises(Exception):
            test_runner.models.TestCaseData()

        test_case = test_runner.models.TestCaseData(**self.script_data_dict)
        self.assertIs(test_case.__str__(), test_case.file_name)
        self.assertEqual(test_case.convert_to_dict(), self.script_data_dict)

    def test_ScenarioData_object(self):
        with self.assertRaises(Exception):
            test_runner.models.ScenarioData()

        scenario_data = test_runner.models.ScenarioData(**self.script_data_dict)
        self.assertIs(scenario_data.__str__(), scenario_data.file_name)
        self.assertEqual(scenario_data.convert_to_dict(), self.scenario_data_dict)

    def test_MasterScenarioData_object(self):
        with self.assertRaises(Exception):
            test_runner.models.MasterScenarioData()

        master_scenario_data = test_runner.models.MasterScenarioData(**self.script_data_dict)
        self.assertIs(master_scenario_data.__str__(), master_scenario_data.file_name)
        self.assertEqual(master_scenario_data.convert_to_dict(), self.master_scenario_data_dict)
