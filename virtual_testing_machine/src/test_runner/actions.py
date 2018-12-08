import os
from .settings import (
    SCENARIOS_DIR,
)
from test_runner.models import (
    RUN_DATA,
    MasterScenarioData,
    ScenarioData,
    TestCase,
)


def run_script(script_path, type=None):
    file_path, file_name = os.path.split(script_path)
    print(f"START  - {file_name}")
    with open(script_path) as script_file:
        script_compiled = compile(script_file.read(), os.path.basename(script_path), 'exec')
    if RUN_DATA.dry_run:
        if type == "master":
            script = MasterScenarioData(file_path, file_name, script_compiled)
        elif type == "scenario":
            script = ScenarioData(file_path, file_name, script_compiled)
        elif type == "test_case":
            script = TestCase(file_path, file_name, script_compiled)
        RUN_DATA.dry_run_data.add_script(script)

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
    RUN_DATA.is_running = False
