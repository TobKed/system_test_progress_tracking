import os


class TestData:
    state = "NA"

    @classmethod
    def print_current_test_status(cls):
        print("Current test status:", cls.state)


def run_script(script_path):
    with open(script_path) as script_file:
        script_compiled = compile(script_file.read(), os.path.basename(script_path),  'exec')
    head, tail = os.path.split(script_path)
    print(f"START  - {tail}")
    exec(script_compiled)
    print(f"FINISH - {tail}")
    

def run_test_case(test_case_path):
    run_script(test_case_path)
                            
                            
def run_test_scenario(test_scenario_path):
    run_script(test_scenario_path)


def run_scenario_master(scenario_master_path):
    run_script(scenario_master_path)
