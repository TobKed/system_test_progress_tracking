import os
from datetime import datetime
import requests
from .settings import (
    SCENARIOS_DIR,
    ENDPOINT_DRY_RUN,
    ENDPOINT_RUN_START,
    ENDPOINT_RUN_STOP,
)
from test_runner.models import (
    RUN_DATA,
    MasterScenarioData,
    ScenarioData,
    TestCaseData,
    WetRunData
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
        elif type_ == "scenario_parent":
            script_obj = ScenarioData(file_path, file_name, script_data)
        elif type_ == "test_case":
            script_obj = TestCaseData(file_path, file_name, script_data)
        RUN_DATA.dry_run_data.add_script(script_obj)

    if  type_ in ["scenario_parent", "master"]:
        exec(script_compiled)
    elif not RUN_DATA.dry_run and type_ =="test_case":

        print("test start")
        RUN_DATA.wet_run_data = WetRunData(file_path=file_path, file_name=file_name)
        wet_run_dict_data_start = RUN_DATA.wet_run_data.get_wet_start_dict()
        print("wet_run_dict_data_start:", wet_run_dict_data_start)
        try:
            r = requests.post(ENDPOINT_RUN_START, json=wet_run_dict_data_start)
            print(r.status_code)
            print(r.content)
        except Exception as e:
            print(e)

        exec(script_compiled)

        print("test finished")
        wet_run_dict_data_stop = RUN_DATA.wet_run_data.get_wet_stop_dict(status=RUN_DATA.last_status)
        print("wet_run_dict_data_stop:", wet_run_dict_data_stop)
        try:
            r = requests.post(ENDPOINT_RUN_STOP, json=wet_run_dict_data_stop)
            print(r.status_code)
            print(r.content)
        except Exception as e:
            print(e)

    print(f"FINISH - {file_name}")


def run_test_case(test_case_path):
    run_script(test_case_path, "test_case")


def run_test_scenario(test_scenario_path):
    run_script(test_scenario_path, "scenario_parent")


def run_scenario_master(scenario_master_path, dry_run=False):
    RUN_DATA.is_running = True
    RUN_DATA.dry_run = dry_run
    run_script(scenario_master_path, "master")
    if dry_run:
        dry_run_dict_data = RUN_DATA.dry_run_data.convert_to_dict()
        print("dry_run_dict_data:", dry_run_dict_data)
        try:
            r = requests.post(ENDPOINT_DRY_RUN, json=dry_run_dict_data)
            print(r.status_code)
            print(r.content)
        except Exception as e:
            print(e)
    RUN_DATA.is_running = False
