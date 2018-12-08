#!/usr/bin/env python3
from test_runner.actions import *
from test_runner.settings import *
from test_runner import TestCaseData


if __name__ == '__main__':
    run_scenario_master(SCENARIO_MASTER, dry_run=True)
    run_scenario_master(SCENARIO_MASTER, dry_run=True)
