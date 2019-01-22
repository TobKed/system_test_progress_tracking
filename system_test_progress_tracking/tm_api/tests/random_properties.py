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
