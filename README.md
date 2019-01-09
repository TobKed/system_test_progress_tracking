## system_test_progress_tracking   
[![Build Status](https:/travis-ci.org/TobKed/system_test_progress_tracking.svg?branch=master)](https:/travis-ci.org/TobKed/system_test_progress_tracking)  [![codecov](https:/codecov.io/gh/TobKed/system_test_progress_tracking/branch/master/graph/badge.svg)](https:/codecov.io/gh/TobKed/system_test_progress_tracking)

## To start 
Prject uses Redis as its backing store. To start a Redis server on port 6379, run the following command:
```bash
docker run -p 6379:6379 -d redis:2.8
```

#### Schemas:
* General scheme
![system_test_progress_tracking_overall_scheme](/docs/img/system_test_progress_tracking_overall_scheme.png)

* Scipts structure in vritual testing machine
![test_scenario_structure](/docs/img/test_scenario_structure.png)

* Database scheme
![db_schema](/docs/img/db_scheme.png)


#### JSON
Information sent by virtual testing machine are sent via POST request to adequate System Test Progress Tracking REST endpoints.


* before first test run (all information about scripts to run)
```js
let data = {
    "machine_name": "machine #1",
    "timestamp": "2018-12-30 13:01:57.461401",
    "master_scenario":
        {
            "file_path": "/virtual_testing_machine/src/test_cases/scenarios",
            "file_name": "scenario_master.py",
            "script": "import os\nfrom run import SCENARIOS_DIR",
            "scenarios":
                [
                    {
                        "file_path": "/virtual_testing_machine/src/test_cases/scenarios",
                        "file_name": "scenario_01_feature_lamp.py",
                        "script": "import os\nfrom run import TEST_CASES_DIR, run_test_case",
                        "tests": [
                            {
                                "file_path": "/PycharmProjects/system",
                                "file_name": "01_01_test_lamp.py",
                                "script": "from time import sleep\n\n\nprint('Start 01_01_test_lamp.py')"
                            },
                            {
                                "file_path": "/virtual_testing_machine/src/test_cases/01_feature_lamp",
                                "file_name": "01_02_test_lamp.py",
                                "script": "from time import sleep\n\nsleep(2)\nRUN_DATA.last_status = 'warning'\n"
                            }
                        ]
                    },
                    {
                        "file_path": "/virtual_testing_machine/src/test_cases/scenarios",
                        "file_name": "scenario_03_feature_trunk.py",
                        "script": "import os\nfrom run import TEST_CASES_DIR, run_test_case\n",
                        "tests": [
                            {
                                "file_path": "/virtual_testing_machine/src/test_cases/02_feature_door",
                                "file_name": "01_01_test_door.py",
                                "script": ""
                            },
                            {
                                "file_path": "/virtual_testing_machine/src/test_cases/02_feature_door",
                                "file_name": "01_02_test_door.py",
                                "script": ""
                            }
                        ]
                    }
                ]
        }
}
```

* before test run
```javascript
let data = {
  "machine_name": "machine #1",
  "file_path": "/virtual_testing_machine/src/test_cases/01_feature_lamp",
  "file_name": "01_01_test_lamp.py",
  "timestamp_start": "2018-12-30 13:01:57.573828"
}
```

* after test run
```javascript
let data = {
  "machine_name": "machine #1",
  "file_path": "/virtual_testing_machine/src/test_cases/01_feature_lamp",
  "file_name": "01_01_test_lamp.py",
  "status": "passed",
  "timestamp_stop": "2018-12-30 13:01:59.622177"
}
```

#### Django lessons learned
* django channels (websockets)
* rest pagination
