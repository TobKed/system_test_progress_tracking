import os


MACHINE_NAME    = "machine #1"

BASE_DIR        = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEST_CASES_DIR  = os.path.join(BASE_DIR, "test_cases")
SCENARIOS_DIR   = os.path.join(TEST_CASES_DIR, "scenarios")
SCENARIO_MASTER = os.path.join(SCENARIOS_DIR, "scenario_master.py")
