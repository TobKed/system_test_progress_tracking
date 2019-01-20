import random
from faker import Faker
from tm_api.models import (
    TEST_STATUS_CHOICES
)


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
