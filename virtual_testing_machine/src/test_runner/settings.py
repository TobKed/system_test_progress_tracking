import os


MACHINE_NAME    = "machine #9"

BASE_DIR        = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEST_CASES_DIR  = os.path.join(BASE_DIR, "test_cases")
SCENARIOS_DIR   = os.path.join(TEST_CASES_DIR, "scenarios")
SCENARIO_MASTER = os.path.join(SCENARIOS_DIR, "scenario_master.py")

ENDPOINT_BASE           = "http://localhost:8000/tm_api/"
ENDPOINT_DRY_RUN        = ENDPOINT_BASE + "dry_run/"
ENDPOINT_RUN_START      = ENDPOINT_BASE + "test_start/"
ENDPOINT_RUN_STOP       = ENDPOINT_BASE + "test_stop/"
ENDPOINT_RUN_EXCEPTION  = ENDPOINT_BASE + "test_exception/"
