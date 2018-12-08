import os


class TestCaseData:
    state = "NA"

    @classmethod
    def print_current_test_status(cls):
        print("Current test status:", cls.state)
