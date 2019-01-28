import random
from faker import Faker
from tm_api.models import (
    TEST_STATUS_CHOICES
)
from . import random_properties


fake = Faker()


def get_random_machine_name():
    return fake.name()


def get_random_status():
    return random.choice(TEST_STATUS_CHOICES)[1]


def get_random_file_name():
    return fake.file_name(extension="py")


def get_random_file_path():
    return "/".join(fake.file_path(depth=10).split("/")[:-1])


def get_random_script():
    return fake.text()


def get_random_time_stamp():
    return fake.date_time()


def get_random_base_script_attrs(**kwargs):
    attrs = {
        "file_name": random_properties.get_random_file_name(),
        "file_path": random_properties.get_random_file_path(),
        "script": random_properties.get_random_script(),
        "_status": random_properties.get_random_status(),
        "timestamp_start": random_properties.get_random_time_stamp(),
        "timestamp_stop": random_properties.get_random_time_stamp()
    }
    attrs.update(**kwargs)
    return attrs


def get_random_dry_run_data_dict(scenarios_count=None, tests_count=None):
    scenarios_count = scenarios_count if scenarios_count else random.rdint(1, 5)
    tests_count = tests_count if tests_count else random.randint(1, 5)
    scenarios = [
        {
            "file_name": get_random_file_name(),
            "file_path": get_random_file_path(),
            "script": get_random_script(),
            "tests": []
        } for _ in range(scenarios_count)
    ]
    for scenario in scenarios:
        scenario["tests"] = [
            {
                "file_name": random_properties.get_random_file_name(),
                "file_path": random_properties.get_random_file_path(),
                "script": random_properties.get_random_script()
            } for _ in range(tests_count)
        ]

    return {
            "machine_name": random_properties.get_random_machine_name(),
            "timestamp": random_properties.get_random_time_stamp(),
            "master_scenario": {
                "file_name": random_properties.get_random_file_name(),
                "file_path": random_properties.get_random_file_path(),
                "script": random_properties.get_random_script(),
                "scenarios": scenarios
            }
        }
