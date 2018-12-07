import unittest


virtual_testing_machine_tests = unittest.TestLoader().discover('virtual_testing_machine/src')
unittest.TextTestRunner(verbosity=2).run(virtual_testing_machine_tests)
