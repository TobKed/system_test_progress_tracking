from django.db import models


class BaseScript(models.Model):
    file_name       = models.CharField(max_length=256)
    file_path       = models.CharField(max_length=1024)
    script          = models.TextField()


class MasterScenario(BaseScript):
    machine_name    = models.CharField(max_length=256)
    time_stamp      = models.DateTimeField(null=True, blank=True)


class Scenario(models.Model):
    master_scenario = models.ForeignKey(MasterScenario, on_delete=models.CASCADE, related_name="scenarios")


class Test(BaseScript):
    scenario        = models.ForeignKey(Scenario, on_delete=models.CASCADE, related_name="tests")
