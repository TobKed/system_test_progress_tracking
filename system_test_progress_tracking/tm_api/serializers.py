from rest_framework import serializers
from .models import (
    Test,
    Scenario,
    MasterScenario
)


class DryRunSerializer(serializers.ModelSerializer):
    class Meta:
        model = MasterScenario
        fields = ('machine_name',)
