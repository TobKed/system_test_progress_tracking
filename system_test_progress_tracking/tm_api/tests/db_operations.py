from random import randint
from django.db import models

from tm_api.models import (
    Machine,
    BaseScript,
)

from . import random_properties


def get_random_obj(model: models.base.ModelBase):
    if not isinstance(model, models.base.ModelBase):
        return AttributeError("is not a model")
    count = model.objects.count()
    if count:
        random_index = randint(0, count - 1)
        return model.objects.all()[random_index]


def create_base_script(
        file_name=random_properties.get_random_file_name(),
        file_path=random_properties.get_random_file_path(),
        script=random_properties.get_random_script(),
        _status=random_properties.get_random_status(),
        timestamp_start=random_properties.get_random_time_stamp(),
        timestamp_stop=random_properties.get_random_time_stamp()):
    return BaseScript.objects.create(
        file_name=file_name,
        file_path=file_path,
        script=script,
        _status=_status,
        timestamp_start=timestamp_start,
        timestamp_stop=timestamp_stop)


def create_machine(machine_name=random_properties.get_random_machine_name()):
    return Machine.objects.create(machine_name=machine_name)
