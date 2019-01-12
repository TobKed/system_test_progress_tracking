from run import RANDOM_MODE

if RANDOM_MODE:
    RUN_DATA.last_status = RUN_DATA.get_random_finished_status()
else:
    RUN_DATA.last_status = "passed"
