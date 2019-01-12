import os
from run import SCENARIOS_DIR, run_test_scenario


run_test_scenario(os.path.join(SCENARIOS_DIR, "scenario_01_feature_lamp.py"))
run_test_scenario(os.path.join(SCENARIOS_DIR, "scenario_02_feature_door.py"))
run_test_scenario(os.path.join(SCENARIOS_DIR, "scenario_03_feature_trunk.py"))
