import os
import requests
from .settings import (
    SCENARIOS_DIR,
    ENDPOINT_DRY_RUN,
)
from test_runner.models import (
    RUN_DATA,
    MasterScenarioData,
    ScenarioData,
    TestCaseData,
)


def run_script(script_path, type_=None):
    file_path, file_name = os.path.split(script_path)
    print(f"START  - {file_name}")
    with open(script_path) as script_file:
        script_data = script_file.read()
        script_compiled = compile(script_data, os.path.basename(script_path), 'exec')
    if RUN_DATA.dry_run:
        if type_ == "master":
            script_obj = MasterScenarioData(file_path, file_name, script_data)
        elif type_ == "scenario":
            script_obj = ScenarioData(file_path, file_name, script_data)
        elif type_ == "test_case":
            script_obj = TestCaseData(file_path, file_name, script_data)
        RUN_DATA.dry_run_data.add_script(script_obj)

    if not RUN_DATA.dry_run or (RUN_DATA.dry_run and SCENARIOS_DIR in script_path):
        exec(script_compiled)
    print(f"FINISH - {file_name}")


def run_test_case(test_case_path):
    run_script(test_case_path, "test_case")


def run_test_scenario(test_scenario_path):
    run_script(test_scenario_path, "scenario")


def run_scenario_master(scenario_master_path, dry_run=False):
    RUN_DATA.is_running = True
    RUN_DATA.dry_run = dry_run
    run_script(scenario_master_path, "master")
    if dry_run:
        #TODO send dry_run_json to
        dry_run_dict_data = RUN_DATA.dry_run_data.convert_to_dict()
        dry_run_dict_data = {
            "machine_name": "test machine name3",
            "timestamp": "2018-12-15 09:42:36.086550",
            "master_scenario": {
                "file_name": "scenario_master.py",
                "file_path": "/home/tobked/PycharmProjects/system_test_progress_tracking/virtual_testing_machine/src/test_cases/scenarios",
                "script": "import os\nfrom run import SCENARIOS_DIR, run_test_scenario\n\n\nrun_test_scenario(os.path.join(SCENARIOS_DIR, \"scenario_01_feature_lamp.py\"))\nrun_test_scenario(os.path.join(SCENARIOS_DIR, \"scenario_02_feature_door.py\"))\nrun_test_scenario(os.path.join(SCENARIOS_DIR, \"scenario_03_feature_trunk.py\"))\n"
            }
        }
        print(dry_run_dict_data)
        try:
            r = requests.post(ENDPOINT_DRY_RUN, json=dry_run_dict_data)
            print(r.status_code)
            print(r.content)
        except Exception as e:
            print(e)
    RUN_DATA.is_running = False
