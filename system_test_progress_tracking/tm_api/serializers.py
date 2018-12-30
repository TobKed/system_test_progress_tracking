from rest_framework import serializers
from .models import (
    Machine,
    Test,
    Scenario,
    MasterScenario,
    DryRunData,
    WAITING
)


class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = ("file_name", "file_path", "script")


class TestModelSerializer(serializers.ModelSerializer):
    timestamp_start = serializers.DateTimeField(format="%d-%m-%Y  %H:%M:%S", required=False, read_only=True)
    timestamp_stop  = serializers.DateTimeField(format="%d-%m-%Y  %H:%M:%S", required=False, read_only=True)

    class Meta:
        model = Test
        fields = ("file_name", "file_path", "script", "timestamp_start", "timestamp_stop")


class TestStartSerializer(serializers.ModelSerializer):
    machine_name    = serializers.CharField()

    class Meta:
        model = Test
        fields = ("machine_name", "file_name", "file_path", "timestamp_start")


class TestStopSerializer(serializers.ModelSerializer):
    machine_name    = serializers.CharField()
    status          = serializers.CharField()

    class Meta:
        model = Test
        fields = ("machine_name", "file_name", "file_path", "timestamp_stop", "status")


class ScenarioSerializer(serializers.ModelSerializer):
    tests = TestSerializer(many=True, required=False)

    class Meta:
        model = Scenario
        fields = ("file_name", "file_path", "script", "tests")


class ScenarioModelSerializer(serializers.ModelSerializer):
    timestamp_start = serializers.DateTimeField(format="%d-%m-%Y  %H:%M:%S", required=False, read_only=True)
    timestamp_stop  = serializers.DateTimeField(format="%d-%m-%Y  %H:%M:%S", required=False, read_only=True)

    class Meta:
        model = Scenario
        fields = ("file_name", "file_path", "script", "timestamp_start", "timestamp_stop")


class MasterScenarioSerializer(serializers.ModelSerializer):
    scenarios       = ScenarioSerializer(many=True, required=False)

    class Meta:
        model = MasterScenario
        fields = ("file_name", "file_path", "script", "scenarios")


class MasterScenarioModelSerializer(serializers.ModelSerializer):
    timestamp_start = serializers.DateTimeField(format="%d-%m-%Y  %H:%M:%S", required=False, read_only=True)
    timestamp_stop  = serializers.DateTimeField(format="%d-%m-%Y  %H:%M:%S", required=False, read_only=True)

    class Meta:
        model = Scenario
        fields = ("file_name", "file_path", "script", "timestamp_start", "timestamp_stop")


class DryRunDataSerializer(serializers.Serializer):
    machine_name    = serializers.CharField(required=False, allow_blank=True, max_length=256)
    timestamp       = serializers.DateTimeField()
    master_scenario = MasterScenarioSerializer()

    def create(self, validated_data):
        default_status = WAITING
        machine_name = validated_data.pop("machine_name", None)
        machine, created = Machine.objects.get_or_create(machine_name=machine_name)
        timestamp = validated_data.pop("timestamp", None)

        master_scenario_data = validated_data.pop('master_scenario')
        scenarios_data = master_scenario_data.pop("scenarios", [])
        master_scenario = MasterScenario.objects.create(_status=default_status, **master_scenario_data)
        for scenario_data in scenarios_data:
            tests_data = scenario_data.pop("tests", [])
            scenario = Scenario.objects.create(master_scenario=master_scenario, _status=default_status, **scenario_data)
            print("scenario:", str(scenario))
            for test_data in tests_data:
                test = Test.objects.create(scenario_parent=scenario, _status=default_status, **test_data)
                print("\ttest:", str(test))

        return DryRunData.objects.create(machine=machine, timestamp=timestamp, master_scenario=master_scenario)
