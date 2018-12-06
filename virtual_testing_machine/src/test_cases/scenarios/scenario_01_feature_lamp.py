import os
from run import TEST_CASES_DIR, run_test_case


FEATURE_DIR = os.path.join(TEST_CASES_DIR, "01_feature_lamp")


run_test_case(os.path.join(FEATURE_DIR, "01_01_test_lamp.py"))
run_test_case(os.path.join(FEATURE_DIR, "01_02_test_lamp.py"))
run_test_case(os.path.join(FEATURE_DIR, "01_03_test_lamp.py"))
run_test_case(os.path.join(FEATURE_DIR, "01_04_test_lamp.py"))
run_test_case(os.path.join(FEATURE_DIR, "01_05_test_lamp.py"))
