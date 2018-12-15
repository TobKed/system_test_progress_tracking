from django.contrib import admin
from .models import (
    Machine,
    Test,
    Scenario,
    MasterScenario,
    DryRunData,
)


admin.site.register(Machine)
admin.site.register(Test)
admin.site.register(Scenario)
admin.site.register(MasterScenario)
admin.site.register(DryRunData)
