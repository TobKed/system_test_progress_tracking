from time import sleep
from run import RANDOM_MODE

print("Start 01_01_test_lamp.py")


print("Turn on lamp")
print("Wait 1 second1")
sleep(1)
print("Verify is lamp on")
print("Turn off lamp")
print("Wait 1 second")
sleep(1)
print("Verify is lamp off")

if RANDOM_MODE:
    RUN_DATA.last_status = RUN_DATA.get_random_finished_status()
else:
    RUN_DATA.last_status = "passed"
