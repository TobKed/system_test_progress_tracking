from rest_framework import serializers
from .models import (
    Machine,
    Test,
    Scenario,
    MasterScenario,
    DryRunData,
)


class MasterScenarioSerializer(serializers.ModelSerializer):

    class Meta:
        model = MasterScenario
        fields = ("file_name", "file_path", "script")


class DryRunDataSerializer(serializers.Serializer):
    machine_name    = serializers.CharField(required=False, allow_blank=True, max_length=256)
    timestamp       = serializers.DateTimeField()
    master_scenario = MasterScenarioSerializer()

    def create(self, validated_data):
        machine_name = validated_data.pop("machine_name", None)
        machine, created = Machine.objects.get_or_create(machine_name=machine_name)
        timestamp = validated_data.pop("timestamp", None)

        master_scenario_data = validated_data.pop('master_scenario')
        master_scenario = MasterScenario.objects.create(**master_scenario_data)
        # scenarios = master_scenario.pop("scenarios")

        return DryRunData.objects.create(machine=machine, timestamp=timestamp, master_scenario=master_scenario)
