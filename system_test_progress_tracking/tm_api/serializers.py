from rest_framework import serializers
from .models import (
    Machine,
    Test,
    Scenario,
    MasterScenario,
    DryRunData,
)


class DryRunDataSerializer(serializers.Serializer):
    machine_name    = serializers.CharField(required=False, allow_blank=True, max_length=256)
    time_stamp      = serializers.DateTimeField()

    def create(self, validated_data):
        machine_name = validated_data.pop("machine_name", None)
        machine, created = Machine.objects.get_or_create(machine_name=machine_name)
        return DryRunData.objects.create(machine=machine, **validated_data)
