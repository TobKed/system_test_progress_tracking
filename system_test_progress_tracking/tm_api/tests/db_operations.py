from random import randint
from django.db import models

from tm_api.models import (
    Machine,
    BaseScript,
    MasterScenario,
    Scenario,
    Test,
    DryRunData
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


def create_scenario(**kwargs):
    attrs = random_properties.get_random_base_script_attrs(**kwargs)
    master_scenario = get_random_obj(MasterScenario)
    return Scenario.objects.create(master_scenario=master_scenario, **attrs)


def create_test(**kwargs):
    attrs = random_properties.get_random_base_script_attrs(**kwargs)
    scenario = get_random_obj(Scenario)
    return Test.objects.create(scenario_parent=scenario, **attrs)


def create_dry_run_data(machine=get_random_obj(Machine),
                        timestamp=random_properties.get_random_time_stamp(),
                        master_scenario=get_random_obj(MasterScenario)):
    return DryRunData.objects.create(machine=machine, timestamp=timestamp, master_scenario=master_scenario)


def populate_db():
    print("populate db ...")

    # Machine
    for _ in range(5):
        Machine.objects.create(machine_name=random_properties.get_random_machine_name())

    # MasterScenario
    for _ in range(30):
        attrs = random_properties.get_random_base_script_attrs()
        MasterScenario.objects.create(**attrs)

    # DryRunData
    for master_scenario in MasterScenario.objects.all():
        machine = get_random_obj(Machine)
        timestamp = random_properties.get_random_time_stamp()
        DryRunData.objects.create(machine=machine, timestamp=timestamp, master_scenario=master_scenario)

    # Scenario
    for _ in range(100):
        attrs = random_properties.get_random_base_script_attrs()
        master_scenario = get_random_obj(MasterScenario)
        Scenario.objects.create(master_scenario=master_scenario, **attrs)

    # Test
    for _ in range(300):
        attrs = random_properties.get_random_base_script_attrs()
        scenario_parent = get_random_obj(Scenario)
        Test.objects.create(scenario_parent=scenario_parent, **attrs)
