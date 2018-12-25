from django.db import models

WAITING = "waiting"
RUNNING = "running"
PASSED  = "passed"
FAILED  = "failed"
WARNING = "warning"
ERROR   = "error"
UNKNOWN = "unknown"
ABORTED = "aborted"

TEST_STATUS_CHOICES = (
    (RUNNING,   "running"),
    (WAITING,   "waiting"),
    (PASSED,    "passed"),
    (FAILED,    "failed"),
    (WARNING,   "warning"),
    (ERROR,     "error"),
    (UNKNOWN,   "unknown"),
    (ABORTED,   "aborted"),
)


class Machine(models.Model):
    machine_name    = models.CharField(max_length=256, unique=True)

    def __str__(self):
        return self.machine_name

    def get_master_scenarios(self):
        return (dry_run_data.master_scenario for dry_run_data in  self.dry_run_datas.all())


class BaseScript(models.Model):
    file_name       = models.CharField(max_length=256)
    file_path       = models.CharField(max_length=1024)
    script          = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.file_name
    

class MasterScenario(BaseScript):
    pass


class DryRunData(models.Model):
    machine         = models.ForeignKey(Machine, on_delete=models.CASCADE, related_name="dry_run_datas")
    timestamp       = models.DateTimeField(null=True, blank=True)
    master_scenario = models.OneToOneField(MasterScenario, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"DryRunData: {self.machine.machine_name} - {self.timestamp}"

    class Meta:
        ordering = ['-timestamp', '-pk']


class Scenario(BaseScript):
    master_scenario = models.ForeignKey(MasterScenario, on_delete=models.CASCADE, related_name="scenarios")


class Test(BaseScript):
    scenario_parent = models.ForeignKey(Scenario, on_delete=models.CASCADE, related_name="tests")
    status          = models.CharField(max_length=9, choices=TEST_STATUS_CHOICES, default="unknown")
