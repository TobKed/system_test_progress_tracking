import os
from .settings import (
    SCENARIOS_DIR,
)
from test_runner.models import RunData


def run_script(script_path):
    head, tail = os.path.split(script_path)
    print(f"START  - {tail}")
    if not RunData.dry_run or (RunData.dry_run and SCENARIOS_DIR in script_path):
        with open(script_path) as script_file:
            script_compiled = compile(script_file.read(), os.path.basename(script_path), 'exec')
        exec(script_compiled)
    print(f"FINISH - {tail}")


def run_dry_script(script_path):
    head, tail = os.path.split(script_path)
    print(f"START DRY - {tail}")
    print(f"FINISH DRY - {tail}")


def run_test_case(test_case_path):
    run_script(test_case_path)


def run_test_scenario(test_scenario_path):
    run_script(test_scenario_path)


def run_scenario_master(scenario_master_path, dry_run=False):
    RunData.dry_run = dry_run
    run_script(scenario_master_path)
