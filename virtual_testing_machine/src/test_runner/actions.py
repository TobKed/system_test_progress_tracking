import os
from .settings import (
    SCENARIOS_DIR,
)
from test_runner.models import (
    RunData,
    DryRunData,
    ScriptData,
    MasterScenarioData,
    ScenarioData
)


DRY_RUN_DATA = None


def run_script(script_path, type=None):
    file_path, file_name = os.path.split(script_path)
    print(f"START  - {file_name}")
    with open(script_path) as script_file:
        script_compiled = compile(script_file.read(), os.path.basename(script_path), 'exec')
    if not RunData.dry_run or (RunData.dry_run and SCENARIOS_DIR in script_path):
        exec(script_compiled)
    print(f"FINISH - {file_name}")


def run_test_case(test_case_path):
    run_script(test_case_path, "test_case")


def run_test_scenario(test_scenario_path):
    run_script(test_scenario_path, "scenario")


def run_scenario_master(scenario_master_path, dry_run=False):
    DRY_RUN_DATA = DryRunData()
    RunData.dry_run = dry_run
    run_script(scenario_master_path, "master")
