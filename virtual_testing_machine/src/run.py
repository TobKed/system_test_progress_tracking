#!/usr/bin/env python3
import os
from test_runner import (
    TestData,
    run_test_case,
    run_test_scenario,
    run_scenario_master
)


BASE_DIR        = os.path.dirname(os.path.abspath(__file__))
TEST_CASES_DIR  = os.path.join(BASE_DIR, "test_cases")
SCENARIOS_DIR   = os.path.join(TEST_CASES_DIR, "scenarios")
SCENARIO_MASTER = os.path.join(SCENARIOS_DIR, "scenario_master.py")

if __name__ == '__main__':
    run_scenario_master(SCENARIO_MASTER)
