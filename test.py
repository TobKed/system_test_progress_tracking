import unittest
import coverage


COV = coverage.coverage(
    omit=[
        'test.py',
        'virtual_testing_machine/src/test/*',
    ]
)
COV.start()


def cov():
    """Runs the unit tests with coverage."""
    virtual_testing_machine_tests = unittest.TestLoader().discover('virtual_testing_machine/src')
    result = unittest.TextTestRunner(verbosity=2).run(virtual_testing_machine_tests)
    if result.wasSuccessful():
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        return 0
    return 1


if __name__ == '__main__':
    cov()
