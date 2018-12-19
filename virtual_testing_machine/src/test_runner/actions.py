import os
from datetime import datetime
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
            "timestamp": str(datetime.now()),
            "master_scenario": {
                "file_name": "scenario_master.py",
                "file_path": "/home/tobked/PycharmProjects/system_test_progress_tracking/virtual_testing_machine/src/test_cases/scenarios",
                "script": "import os\nfrom run import SCENARIOS_DIR, run_test_scenario\n\n\nrun_test_scenario(os.path.join(SCENARIOS_DIR, \"scenario_01_feature_lamp.py\"))\nrun_test_scenario(os.path.join(SCENARIOS_DIR, \"scenario_02_feature_door.py\"))\nrun_test_scenario(os.path.join(SCENARIOS_DIR, \"scenario_03_feature_trunk.py\"))\n",
                "scenarios": [
                    {
                        "file_name": "scenario_01_feature_lamp.py",
                        "file_path": "/home/tobked/PycharmProjects/system_test_progress_tracking/virtual_testing_machine/src/test_cases/scenarios",
                        "script": "import os\nfrom run import TEST_CASES_DIR, run_test_case\n\n\nFEATURE_DIR = os.path.join(TEST_CASES_DIR, \"01_feature_lamp\")\n\n\nrun_test_case(os.path.join(FEATURE_DIR, \"01_01_test_lamp.py\"))\nrun_test_case(os.path.join(FEATURE_DIR, \"01_02_test_lamp.py\"))\nrun_test_case(os.path.join(FEATURE_DIR, \"01_03_test_lamp.py\"))\nrun_test_case(os.path.join(FEATURE_DIR, \"01_04_test_lamp.py\"))\nrun_test_case(os.path.join(FEATURE_DIR, \"01_05_test_lamp.py\"))\n",
                        "tests": [
                            {
                                "file_name": "01_01_test_lamp.py",
                                "file_path": "/home/tobked/PycharmProjects/system_test_progress_tracking/virtual_testing_machine/src/test_cases/01_feature_lamp",
                                "script": "from time import sleep\n\nprint(\"Start 01_01_test_lamp.py\")\n\n\nprint(\"Turn on lamp\")\nprint(\"Wait 1 second1\")\nsleep(1)\nprint(\"Verify is lamp on\")\nprint(\"Turn off lamp\")\nprint(\"Wait 1 second\")\nsleep(1)\nprint(\"Verify is lamp off\")\n"
                            },
                            {
                                "file_name": "01_02_test_lamp.py",
                                "file_path": "/home/tobked/PycharmProjects/system_test_progress_tracking/virtual_testing_machine/src/test_cases/01_feature_lamp",
                                "script": ""
                            },
                        ]
                    },
                    {
                        "file_name": "scenario_02_feature_door.py",
                        "file_path": "/home/tobked/PycharmProjects/system_test_progress_tracking/virtual_testing_machine/src/test_cases/scenarios",
                        "script": "import os\nfrom run import TEST_CASES_DIR, run_test_case\n\n\nFEATURE_DIR = os.path.join(TEST_CASES_DIR, \"02_feature_door\")\n\n\nrun_test_case(os.path.join(FEATURE_DIR, \"01_01_test_door.py\"))\nrun_test_case(os.path.join(FEATURE_DIR, \"01_02_test_door.py\"))\n",
                        "tests": [
                            {
                                "file_name": "01_01_test_door.py",
                                "file_path": "/home/tobked/PycharmProjects/system_test_progress_tracking/virtual_testing_machine/src/test_cases/02_feature_door",
                                "script": ""
                            },
                            {
                                "file_name": "01_02_test_door.py",
                                "file_path": "/home/tobked/PycharmProjects/system_test_progress_tracking/virtual_testing_machine/src/test_cases/02_feature_door",
                                "script": ""
                            }
                        ]
                    },
                ],
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
