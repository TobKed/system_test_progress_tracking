import os
import sys
import unittest
import coverage
import django
from django.conf import settings
from django.test.utils import get_runner
from django.utils.crypto import get_random_string


VIRTUAL_TESTING_MACHINE_DIR = "virtual_testing_machine/"
DJANGO_PROJECT_DIR = os.path.join(os.getcwd(), "system_test_progress_tracking/")

# for django setup proper imports
sys.path.insert(0, DJANGO_PROJECT_DIR)


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
    testing_machine_result = testing_machine_test()
    progress_tracking_failures = progress_tracking_test()
    if testing_machine_result.wasSuccessful() and not progress_tracking_failures:
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        return 0
    return 1


def testing_machine_test():
    virtual_testing_machine_tests = unittest.TestLoader().discover(VIRTUAL_TESTING_MACHINE_DIR)
    result = unittest.TextTestRunner(verbosity=2).run(virtual_testing_machine_tests)
    return result


def progress_tracking_test():
    os.environ['DJANGO_SETTINGS_MODULE'] = 'stpt.settings'
    os.environ['DJANGO_SECRET_KEY'] = get_random_string()
    django.setup()
    TestRunner = get_runner(settings)
    test_runner = TestRunner(verbosity=2)
    failures = test_runner.run_tests(['tm_api.tests'])
    return failures


if __name__ == '__main__':
    cov()
