from django.db import models

RUNNING = "running"
ABORTED = "aborted"
FAILED  = "failed"
ERROR   = "error"
WARNING = "warning"
WAITING = "waiting"
UNKNOWN = "unknown"
PASSED  = "passed"

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

STATUS_PRIORITY = [
    RUNNING,
    ABORTED,
    FAILED,
    ERROR,
    WARNING,
    WAITING,
    UNKNOWN,
    PASSED
]


class Machine(models.Model):
    machine_name    = models.CharField(max_length=256, unique=True)

    def __str__(self):
        return self.machine_name

    def get_master_scenarios(self):
        return (dry_run_data.master_scenario for dry_run_data in self.dry_run_datas.all())

    def get_last_master_scenario_status(self):
        dry_run_data = self.dry_run_datas.first()
        status = dry_run_data.master_scenario.tests_status if dry_run_data else "not-available"
        return status


class BaseScript(models.Model):
    file_name       = models.CharField(max_length=256)
    file_path       = models.CharField(max_length=1024)
    script          = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.file_name

    class Meta:
        ordering = ['-pk']


class MasterScenario(BaseScript):
    @property
    def scenarios_count(self):
        return self.scenarios.all().count()

    @property
    def tests_count(self):
        return sum([scenario.tests_count for scenario in self.scenarios.all()])

    @property
    def tests_status(self):
        tests_statuses = [scenario.tests_status for scenario in self.scenarios.all()]
        for status in STATUS_PRIORITY:
            if status in tests_statuses:
                return status
        return "not-available"

    @property
    def tests_statistics(self):
        statistics = {}
        tests_statuses = [test.status for scenario in self.scenarios.all() for test in scenario.tests.all()]
        for status in STATUS_PRIORITY:
            statistics[status] = tests_statuses.count(status)
        return statistics

    class Meta:
        ordering = ['-pk']


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

    @property
    def tests_count(self):
        return self.tests.all().count()

    @property
    def tests_status(self):
        tests_statuses = [test.status for test in self.tests.all()]
        for status in STATUS_PRIORITY:
            if status in tests_statuses:
                return status
        return "not-available"

    class Meta:
        ordering = ['-pk']


class Test(BaseScript):
    scenario_parent = models.ForeignKey(Scenario, on_delete=models.CASCADE, related_name="tests")
    status          = models.CharField(max_length=9, choices=TEST_STATUS_CHOICES, default="unknown")

    class Meta:
        ordering = ['-pk']
