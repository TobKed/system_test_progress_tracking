import os


def run_script(script_path, dry_run):
    head, tail = os.path.split(script_path)
    print(f"START  - {tail}")
    # if not dry_run and
    with open(script_path) as script_file:
        script_compiled = compile(script_file.read(), os.path.basename(script_path), 'exec')
    exec(script_compiled)
    print(f"FINISH - {tail}")


def run_dry_script(script_path):
    head, tail = os.path.split(script_path)
    print(f"START DRY - {tail}")
    print(f"FINISH DRY - {tail}")


def run_test_case(test_case_path, dry_run=False):
    run_script(test_case_path, dry_run)


def run_test_scenario(test_scenario_path, dry_run=False):
    run_script(test_scenario_path, dry_run)


def run_scenario_master(scenario_master_path, dry_run=False):
    run_script(scenario_master_path, dry_run)
