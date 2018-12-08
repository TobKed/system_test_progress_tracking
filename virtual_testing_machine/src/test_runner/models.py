from .settings import MACHINE_NAME
import json
from datetime import datetime


class RunData:
    def __init__(self):
        self.dry_run_active = False
        self.dry_run_data = None
        self.is_running = False

    @property
    def dry_run(self):
        return self.dry_run_active

    @dry_run.setter
    def dry_run(self, state):
        if state:
            self.dry_run_data = DryRunData()
        self.dry_run_active = state


RUN_DATA = RunData()


class DryRunData:
    """ class used to collect data about all test cases during dry run and generate JSON """
    def __init__(self):
        self.machine_name = MACHINE_NAME
        self.time_stamp = None
        self.master_scenario = None

    def add_script(self, script_object):
        if isinstance(script_object, MasterScenarioData):
            self.master_scenario = script_object
        elif isinstance(script_object, ScenarioData):
            self.master_scenario.scenarios.append(script_object)
        elif isinstance(script_object, TestCase):
            self.master_scenario.scenarios[-1].tests.append(TestCase)
        else:
            raise TypeError("Unknown script type")

    def toJSON(self):
        self.time_stamp = datetime.now()
        return json.dumps(self, default=lambda o: vars(o), sort_keys=True, indent=4)


class ScriptData:
    def __init__(self, file_path, file_name, script):
        self.file_path = file_path
        self.file_name = file_name
        self.script = script

    def toJSON(self):
        return json.dumps(self, default=lambda o: vars(o), sort_keys=True, indent=4)

    def __str__(self):
        return self.file_name


class MasterScenarioData(ScriptData):
    def __init__(self, file_path, file_name, script, scenarios=None):
        self.scenarios = scenarios if scenarios else []
        super().__init__(file_path, file_name, script)

    def toJSON(self):
        self.scenarios = [scenario.toJson() for scenario in self.scenarios] if self.scenarios else None
        super().toJSON()
        

class ScenarioData(ScriptData):
    def __init__(self, file_path, file_name, script, tests=None):
        self.tests = tests if tests else []
        super().__init__(file_path, file_name, script)

    def toJSON(self):
        self.tests = [test.toJson() for test in self.tests] if self.tests else None
        super().toJSON()


class TestCase(ScriptData):
    pass
