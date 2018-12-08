class RunData:
    dry_run = False


class TestData:
    state = "NA"

    @classmethod
    def print_last_test_status(cls):
        print("Last test status:", cls.state)
