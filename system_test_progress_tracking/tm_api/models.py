import operator
from django.db import models, IntegrityError
from django.db.models import Q
from functools import reduce

RUNNING     = "running"
CANCELLED   = "cancelled"
FAILED      = "failed"
ERROR       = "error"
WARNING     = "warning"
WAITING     = "waiting"
UNKNOWN     = "unknown"
PASSED      = "passed"

TEST_STATUS_CHOICES = (
    (RUNNING,   "running"),
    (CANCELLED, "cancelled"),
    (FAILED,    "failed"),
    (ERROR,     "error"),
    (WARNING,   "warning"),
    (WAITING,   "waiting"),
    (UNKNOWN,   "unknown"),
    (PASSED,    "passed"),
)

STATUS_PRIORITY = [
    CANCELLED,
    RUNNING,
    WAITING,
    UNKNOWN,
    FAILED,
    ERROR,
    WARNING,
    PASSED
]

STATUS_ONGOING = [
    RUNNING,
    WAITING
]

STATUS_FINISHED = [
    CANCELLED,
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
    _status         = models.CharField(max_length=9, choices=TEST_STATUS_CHOICES, default="unknown", db_column="status")
    file_name       = models.CharField(max_length=256)
    file_path       = models.CharField(max_length=1024)
    script          = models.TextField(blank=True, null=True)
    timestamp_start = models.DateTimeField(blank=True, null=True)
    timestamp_stop  = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['-pk']

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
            self.objects.update(_status=value)

    def __str__(self):
        return self.file_name


class MasterScenario(BaseScript):

    @property
    def scenarios_count(self):
        return self.scenarios.all().count()

    @property
    def tests_count(self):
        return sum([scenario.tests_count for scenario in self.scenarios.all()])

    @property
    def tests_status(self):
        if self._status is None:
            self.objects.update(_status=self._get_status())
        return self._status

    @property
    def tests_statistics(self):
        statistics = {}
        tests_statuses = [test.status for scenario in self.scenarios.all() for test in scenario.tests.all()]
        for status in STATUS_PRIORITY:
            statistics[status] = tests_statuses.count(status)
        return statistics

    def _get_status(self):
        tests_statuses = [scenario.tests_status for scenario in self.scenarios.all()]
        for status in STATUS_PRIORITY:
            if status in tests_statuses:
                return status
        else:
            return "unknown"

    def update_status(self):
        self.objects.update(_status=self._get_status())
        self.master_scenario.update_status()

    def _set_all_ongoing_tests_to_value(self, value):
        for scenario in self.scenarios.all():
            for test in scenario.tests.all():
                if test.status in STATUS_ONGOING:
                    test.status = value
            scenario.update_status()
        self.update_status()

    def set_all_ongoing_tests_to_unknown(self):
        self._set_all_ongoing_tests_to_value(UNKNOWN)

    def set_all_ongoing_tests_to_cancelled(self):
        self._set_all_ongoing_tests_to_value(CANCELLED)

    class Meta:
        ordering = ['-pk']


class DryRunData(models.Model):
    machine         = models.ForeignKey(Machine, on_delete=models.CASCADE, related_name="dry_run_datas")
    timestamp       = models.DateTimeField(null=True, blank=True)
    master_scenario = models.OneToOneField(MasterScenario, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"DryRunData: {self.machine.machine_name} - {self.timestamp}"

    def save(self, *args, **kwargs):
        query = reduce(operator.or_, (Q(master_scenario___status__icontains=status) for status in STATUS_ONGOING))
        for dry_run_data in DryRunData.objects.filter(query, machine=self.machine):
            dry_run_data.master_scenario.set_all_ongoing_tests_to_unknown()
        return super().save(*args, **kwargs)

    class Meta:
        ordering = ['-timestamp', '-pk']


class Scenario(BaseScript):
    master_scenario = models.ForeignKey(MasterScenario, on_delete=models.CASCADE, related_name="scenarios")

    @property
    def tests_count(self):
        return self.tests.all().count()

    def _get_status(self):
        tests_statuses = [test.status for test in self.tests.all()]
        for status in STATUS_PRIORITY:
            if status in tests_statuses:
                return status
        else:
            return "unknown"

    @property
    def status(self):
        if self._status is None:
            self.objects.update(_status=self._get_status())
        return self._status

    def update_status(self):
        self.objects.update(_status=self._get_status())
        self.master_scenario.update_status()

    class Meta:
        ordering = ['-pk']


class Test(BaseScript):
    scenario_parent        = models.ForeignKey(Scenario, on_delete=models.CASCADE, related_name="tests")

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        if value in [i[0] for i in TEST_STATUS_CHOICES]:
            self._status = value
            self.save()
            if value == CANCELLED:
                self.scenario_parent.master_scenario.set_all_ongoing_tests_to_cancelled()
            else:
                self.scenario_parent.update_status()
        else:
            raise IntegrityError("wrong status cannot be set")

    class Meta:
        ordering = ['-pk']
