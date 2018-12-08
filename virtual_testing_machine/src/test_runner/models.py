from .settings import MACHINE_NAME
import json
from datetime import datetime


class RunData:
    dry_run = False


class DryRunData:
    def __init__(self):
        self.machine_name = MACHINE_NAME
        self.time_stamp = None
        self.master_scenario = None

    def toJSON(self):
        self.time_stamp = datetime.now()
        return json.dumps(self, default=lambda o: vars(o), sort_keys=True, indent=4)


class TestCaseData:
    def __init__(self, file_path, file_name, script):
        self.file_path = file_path
        self.file_name = file_name
        self.script = script

    def toJSON(self):
        return json.dumps(self, default=lambda o: vars(o), sort_keys=True, indent=4)


class MasterScenarioData(TestCaseData):
    def __init__(self, file_path, file_name, script, tests=None):
        self.tests = tests if tests else []
        super().__init__(file_path, file_name, script)

    def toJSON(self):
        self.tests = [test.toJson() for test in self.tests] if self.tests else None
        return json.dumps(self, default=lambda o: vars(o), sort_keys=True, indent=4)


class TestData:
    state = "NA"

    @classmethod
    def print_last_test_status(cls):
        print("Last test status:", cls.state)
