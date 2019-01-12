from time import sleep

sleep(2)
# RUN_DATA.last_status = "passed"
RUN_DATA.last_status = RUN_DATA.get_random_finished_status()
