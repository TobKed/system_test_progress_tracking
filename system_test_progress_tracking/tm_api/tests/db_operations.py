from random import randint
from django.db import models

from tm_api.models import (
    Machine,
    BaseScript,
    MasterScenario
)

from . import random_properties


def get_random_obj(model: models.base.ModelBase):
    if not isinstance(model, models.base.ModelBase):
        return AttributeError("is not a model")
    count = model.objects.count()
    if count:
        random_index = randint(0, count - 1)
        return model.objects.all()[random_index]


def create_machine(machine_name=random_properties.get_random_machine_name()):
    return Machine.objects.create(machine_name=machine_name)


def create_base_script(**kwargs):
    attrs = random_properties.get_random_base_script_attrs(**kwargs)
    return BaseScript.objects.create(**attrs)


def create_master_scenario(**kwargs):
    attrs = random_properties.get_random_base_script_attrs(**kwargs)
    return MasterScenario.objects.create(**attrs)
