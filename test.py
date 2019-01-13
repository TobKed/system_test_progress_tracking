import unittest
import coverage

import django
from django.conf import settings
from django.test.utils import get_runner
from system_test_progress_tracking.stpt.settings import DATABASES, INSTALLED_APPS, ROOT_URLCONF

SETTINGS_DICT = {
    "DATABASES": DATABASES,
    "INSTALLED_APPS": ['django.contrib.admin',
                       'django.contrib.auth',
                       'django.contrib.contenttypes',
                       'django.contrib.sessions',
                       'django.contrib.messages',
                       'django.contrib.staticfiles',
                       'channels',
                       'django_extensions',
                       'rest_framework',
                       'crispy_forms',
                       'system_test_progress_tracking.stpt',
                       'system_test_progress_tracking.tm_api',
                       'system_test_progress_tracking.users',
                       'system_test_progress_tracking.progress_tracking'],
    "ROOT_URLCONF": 'system_test_progress_tracking.tm_api.urls'
}


COV = coverage.coverage(
    omit=[
        'test.py',
        'virtual_testing_machine/test/*',
        'venv/*',
    ]
)
COV.start()


def cov():
    """Runs the unit tests with coverage."""
    virtual_testing_machine_tests = unittest.TestLoader().discover('virtual_testing_machine/')
    result = unittest.TextTestRunner(verbosity=2).run(virtual_testing_machine_tests)
    django_failures = test_django()
    if result.wasSuccessful() and not django_failures:
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        return 0
    return 1


def test_django():
    settings.configure(**SETTINGS_DICT)
    django.setup()
    TestRunner = get_runner(settings)
    test_runner = TestRunner(verbosity=2, interactive=True)
    failures = test_runner.run_tests(['system_test_progress_tracking.tm_api.tests'])
    return failures


if __name__ == '__main__':
    cov()
