import operator
from django.db import models, IntegrityError
from django.db.models import Q
from django.urls import reverse
from functools import reduce
from datetime import datetime


CANCELLED   = "cancelled"
RUNNING     = "running"
WAITING     = "waiting"
UNKNOWN     = "unknown"
FAILED      = "failed"
ERROR       = "error"
WARNING     = "warning"
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
    UNKNOWN,
    WARNING,
    PASSED,
]


class Machine(models.Model):
    machine_name    = models.CharField(max_length=256, unique=True)

    def __str__(self):
        return self.machine_name

    @property
    def master_scenarios(self):
        return MasterScenario.objects.filter(dryrundata__machine=self)

    def get_tests(self, file_name, file_path, status=WAITING):
        return Test.objects.filter(
            file_name=file_name,
            file_path=file_path,
            scenario_parent__master_scenario__dryrundata__in=self.dry_run_datas.all(),
            scenario_parent___status__in=STATUS_ONGOING,
            _status=status
        )

    @property
    def last_master_scenario(self):
        dry_run_data = self.dry_run_datas.first()
        return dry_run_data.master_scenario if dry_run_data else None

    def get_last_master_scenario_status(self):
        dry_run_data = self.dry_run_datas.first()
        status = dry_run_data.master_scenario.tests_status if dry_run_data else "not-available"
        return status

    def get_absolute_url(self):
        return reverse("machine-detail-view", kwargs={"pk": self.pk})


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
        if value in [i[0] for i in TEST_STATUS_CHOICES]:
            self._status = value
            self.save()
        else:
            raise IntegrityError("wrong status cannot be set")

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
            self._status=self._get_status()
        return self._status

    @property
    def tests_statistics(self):
        statistics = {}
        tests_statuses = [test.status for scenario in self.scenarios.all() for test in scenario.tests.all()]
        for status in STATUS_PRIORITY:
            statistics[status] = tests_statuses.count(status)
        return statistics

    def _get_status(self):
        tests_statuses = [scenario.status for scenario in self.scenarios.all()]
        for status in STATUS_PRIORITY:
            if status in tests_statuses:
                return status
        else:
            return "unknown"

    def update_status(self):
        _status = self._get_status()
        self._status = _status
        if self.timestamp_start and _status in STATUS_FINISHED:
            self.timestamp_stop = datetime.now()
        if not self.timestamp_start and _status in STATUS_ONGOING:
            self.timestamp_start = datetime.now()
        self.save()

    def set_all_ongoing_tests_to_value(self, value):
        for scenario in self.scenarios.all():
            for test in scenario.tests.all():
                if test.status in STATUS_ONGOING:
                    test.status = value
            scenario.update_status()
        self.update_status()

    def set_all_ongoing_tests_to_unknown(self):
        self.set_all_ongoing_tests_to_value(UNKNOWN)

    def set_all_ongoing_tests_to_cancelled(self):
        self.set_all_ongoing_tests_to_value(CANCELLED)

    def set_only_last_running_test(self):
        running_tests = Test.objects.filter(scenario_parent__in=self.scenarios.all(), _status=RUNNING)
        count = running_tests.count()
        if count > 1:
            for running_test in running_tests[:count-1]:
                running_test.status = UNKNOWN

    class Meta:
        ordering = ['-pk']


class DryRunData(models.Model):
    machine         = models.ForeignKey(Machine, on_delete=models.CASCADE, related_name="dry_run_datas")
    timestamp       = models.DateTimeField(null=True, blank=True)
    master_scenario = models.OneToOneField(MasterScenario, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"DryRunData: {self.machine.machine_name} - {self.timestamp}"

    def save(self, *args, **kwargs):
        """
        before saving new dry run data
            if any ongoing tests on the machine
            then set all ongoing tests to unknown
        """
        query = reduce(operator.or_, (Q(master_scenario___status__icontains=status) for status in STATUS_ONGOING))
        for dry_run_data in DryRunData.objects.filter(query, machine=self.machine):
            dry_run_data.master_scenario.set_all_ongoing_tests_to_unknown()
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("dry-run-data-detail-view", kwargs={"pk": self.pk})

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
            self._status=self._get_status()
        return self._status

    def update_status(self):
        _status = self._get_status()
        self._status = _status
        if self.timestamp_start and _status in STATUS_FINISHED:
            self.timestamp_stop = datetime.now()
        if not self.timestamp_start and _status in STATUS_ONGOING:
            self.timestamp_start = datetime.now()
        self.save()
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
            if value == RUNNING:
                self.scenario_parent.master_scenario.set_only_last_running_test()
                self.scenario_parent.update_status()
            else:
                self.scenario_parent.update_status()
        else:
            raise IntegrityError("wrong status cannot be set")

    class Meta:
        ordering = ['-pk']
