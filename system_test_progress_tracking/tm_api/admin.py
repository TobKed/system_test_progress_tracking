from django.contrib import admin
from .models import Test, Scenario, MasterScenario


admin.site.register(Test)
admin.site.register(Scenario)
admin.site.register(MasterScenario)
