import os
from run import TEST_CASES_DIR, run_test_case


FEATURE_DIR = os.path.join(TEST_CASES_DIR, "03_feature_trunk")


run_test_case(os.path.join(FEATURE_DIR, "01_01_test_trunk.py"))
run_test_case(os.path.join(FEATURE_DIR, "01_01_test_trunk.py"))
