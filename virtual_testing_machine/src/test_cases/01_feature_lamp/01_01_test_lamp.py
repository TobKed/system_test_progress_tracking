from test_runner.models import TestData
from time import sleep

print("Start 01_01_test_lamp.py")


print("Turn on lamp")
print("Wait 1 second1")
sleep(1)
print("Verify is lamp on")
print("Turn off lamp")
print("Wait 1 second")
sleep(1)
print("Verify is lamp off")

TestData.state = "passed"
