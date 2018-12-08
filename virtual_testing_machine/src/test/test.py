import unittest
import os
from time import time
from unittest.mock import MagicMock
import run
import test_runner.actions


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

    @unittest.mock.patch("builtins.print")
    def test_print_current_test_status(self, mocked_print):
        test_string = "test status"
        run.TestCaseData.state = test_string
        run.TestCaseData.print_current_test_status()
        mocked_print.assert_called_once_with('Current test status:', test_string)

    def test_run_test_case(self):
        time_start = time()
        test_runner.actions.run_test_case(self.test_case_path)
        time_end = time()
        execution_time = time_end - time_start
        self.assertTrue(1.5 < execution_time < 2.5)

    @unittest.mock.patch("test_runner.actions.run_script")
    def test_runners(self, mocked_run_script):
        test_path = run.SCENARIO_MASTER
        test_runner.actions.run_test_case(test_path, dry_run=False)
        test_runner.actions.run_test_scenario(test_path, dry_run=False)
        test_runner.actions.run_scenario_master(test_path, dry_run=False)
        mocked_run_script.assert_called_with(test_path, False)
        self.assertEqual(mocked_run_script.call_args_list, [unittest.mock.call(test_path, False)]*3)
        self.assertEqual(mocked_run_script.call_count, 3)
