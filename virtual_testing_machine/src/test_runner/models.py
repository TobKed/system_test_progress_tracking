from .settings import MACHINE_NAME
import json
from datetime import datetime


class RunData:
    def __init__(self):
        self._dry_run_active = False
        self.dry_run_data = None
        self.is_running = False

    @property
    def dry_run(self):
        return self._dry_run_active

    @dry_run.setter
    def dry_run(self, state):
        if state:
            self.dry_run_data = DryRunData()
        self._dry_run_active = state


RUN_DATA = RunData()


class DryRunData:
    """ class used to collect data about all test cases during dry run and generate JSON """
    def __init__(self):
        self.machine_name = MACHINE_NAME
        self.timestamp = datetime.now()
        self.master_scenario = None

    def add_script(self, script_object):
        if isinstance(script_object, MasterScenarioData):
            self.master_scenario = script_object
        elif isinstance(script_object, ScenarioData):
            self.master_scenario.scenarios.append(script_object)
        elif isinstance(script_object, TestCaseData):
            self.master_scenario.scenarios[-1].tests.append(script_object)
        else:
            raise TypeError("Unknown script type")

    def convert_to_dict(self):
        timestamp = str(self.timestamp)
        master_scenario = self.master_scenario.convert_to_dict()
        return {**self.__dict__, **{"master_scenario": master_scenario, "timestamp": timestamp}}

    def toJSON(self):
        return json.dumps(self.convert_to_dict(), sort_keys=True, indent=4)


class ScriptData:
    def __init__(self, file_path, file_name, script):
        self.file_path = file_path
        self.file_name = file_name
        self.script = script

    def convert_to_dict(self):
        return self.__dict__

    def __str__(self):
        return self.file_name


class MasterScenarioData(ScriptData):
    def __init__(self, file_path, file_name, script):
        self.scenarios = []
        super().__init__(file_path, file_name, script)

    def convert_to_dict(self):
        scenarios = [scenario.convert_to_dict() for scenario in self.scenarios] if self.scenarios else None
        return {**self.__dict__, **{"scenarios": scenarios}}
        

class ScenarioData(ScriptData):
    def __init__(self, file_path, file_name, script):
        self.tests = []
        super().__init__(file_path, file_name, script)

    def convert_to_dict(self):
        tests = [test.convert_to_dict() for test in self.tests] if self.tests else None
        return {**self.__dict__, **{"tests": tests}}


class TestCaseData(ScriptData):
    pass
