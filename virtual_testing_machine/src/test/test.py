import unittest
import os
import run
from time import time
from unittest.mock import MagicMock


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
        run.TestData.state = test_string
        run.TestData.print_current_test_status()
        mocked_print.assert_called_once_with('Current test status:', test_string)

    def test_run_test_case(self):
        time_start = time()
        run.run_test_case(self.test_case_path)
        time_end = time()
        execution_time = time_end - time_start
        self.assertTrue(1.5 < execution_time < 2.5)
