#!/usr/bin/env python3
import os
from test_runner.actions import (
    run_scenario_master
)
from test_runner import TestCaseData


MACHINE_NAME    = "machine #1"

BASE_DIR        = os.path.dirname(os.path.abspath(__file__))
TEST_CASES_DIR  = os.path.join(BASE_DIR, "test_cases")
SCENARIOS_DIR   = os.path.join(TEST_CASES_DIR, "scenarios")
SCENARIO_MASTER = os.path.join(SCENARIOS_DIR, "scenario_master.py")

if __name__ == '__main__':
    run_scenario_master(SCENARIO_MASTER, dry_run=True)
    run_scenario_master(SCENARIO_MASTER, dry_run=True)
