from django.db import models, IntegrityError

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

STATUS_ONGOING = [
    RUNNING,
    WAITING
]

STATUS_FINISHED = [
    ABORTED,
    FAILED,
    ERROR,
    WAITING,
    UNKNOWN,
    PASSED,
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
    _tests_status = models.CharField(max_length=9, choices=TEST_STATUS_CHOICES, null=True, blank=True, default=None, db_column="tests_status")

    @property
    def scenarios_count(self):
        return self.scenarios.all().count()

    @property
    def tests_count(self):
        return sum([scenario.tests_count for scenario in self.scenarios.all()])

    def _get_tests_status(self):
        tests_statuses = [scenario.tests_status for scenario in self.scenarios.all()]
        for status in STATUS_PRIORITY:
            if status in tests_statuses:
                return status
        else:
            return "unknown"

    @property
    def tests_status(self):
        if self._tests_status is None:
            self._tests_status = self._get_tests_status()
            self.save()
        return self._tests_status

    def update_tests_status(self):
        self._tests_status = self._get_tests_status()
        self.save()

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
    _tests_status   = models.CharField(max_length=9, choices=TEST_STATUS_CHOICES, null=True, blank=True, default=None, db_column="tests_status")

    @property
    def tests_count(self):
        return self.tests.all().count()

    def _get_tests_status(self):
        tests_statuses = [test.status for test in self.tests.all()]
        for status in STATUS_PRIORITY:
            if status in tests_statuses:
                return status
        else:
            return "unknown"

    @property
    def tests_status(self):
        if self._tests_status is None:
            self._tests_status = self._get_tests_status()
            self.save()
        return self._tests_status

    def update_tests_status(self):
        self._tests_status = self._get_tests_status()
        self.save()
        self.master_scenario.update_tests_status()

    class Meta:
        ordering = ['-pk']


class Test(BaseScript):
    scenario_parent = models.ForeignKey(Scenario, on_delete=models.CASCADE, related_name="tests")
    _status          = models.CharField(max_length=9, choices=TEST_STATUS_CHOICES, default="unknown", db_column="status")

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        if value in [i[0] for i in TEST_STATUS_CHOICES]:
            self._status = value
            self.save()
            self.scenario_parent.update_tests_status()
        else:
            raise IntegrityError("wrong status cannot be set")

    class Meta:
        ordering = ['-pk']
