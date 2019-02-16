# System Test Progress Tracking   [![Build Status](https://travis-ci.org/TobKed/system_test_progress_tracking.svg?branch=master)](https://travis-ci.org/TobKed/system_test_progress_tracking) [![codecov](https://codecov.io/gh/TobKed/system_test_progress_tracking/branch/master/graph/badge.svg)](https://codecov.io/gh/TobKed/system_test_progress_tracking) ![](https://img.shields.io/github/license/TobKed/system_test_progress_tracking.svg?style=flat)
Application for system tests monitoring. The physical machines used for system testing have a built-in python
         interpreter, however when the test suite is running there is no convenient way to track the test status. My 
         application solved this problem. A modified test runner sends information in JSON format to the server where 
         the Django application received and processed them. Users can browse not only the previous results, but also 
         observe a live preview of the test suite currently running. 

## How to run project

### Install requirements
```
pip install -r requirements.txt
```

### Environment variables
```
DJANGO_SECRET_KEY='dont-tell-eve'
```

### Redis instance
Project uses Redis as its backing store. To start a Redis server on port 6379, run the following command:
```bash
docker run -p 6379:6379 -d redis:2.8
```

### Run Django server
```bash
python system_test_progress_tracking/manage.py runserver
```

### Run Virtual System Testing Machine
```bash
python virtual_testing_machine/run.py
```

## Schemas:
* General scheme
![system_test_progress_tracking_overall_scheme](/docs/img/system_test_progress_tracking_overall_scheme.png)

* Virtual testing machine scripts structure
![test_scenario_structure](/docs/img/test_scenario_structure.png)

* Database scheme
![db_schema](/docs/img/db_scheme.png)

## Virtual Testing Machine
### Scripts execution hierarchy (simplified functions)
```yaml
run_scenario_master("scenario_master.py")
    run_test_scenario("scenario_01.py")
        run_test_case("01_01_test.py")
        run_test_case("01_02_test.py")
        run_test_case("01_03_test.py")
        run_test_case("01_04_test.py")
        run_test_case("01_05_test.py")
    run_test_scenario(, "scenario_02.py")
        run_test_case("01_01_test.py")
        run_test_case("01_02_test.py")
    run_test_scenario(, "scenario_03.py")
        run_test_case("01_01.py")
        run_test_case("01_01.py")
```

### JSON
Information from Virtual System Testing Machine is sent via POST request to adequate System Test Progress Tracking REST endpoints.

* DRY RUN - run without executing tests, used to build all information about scripts to run
```javascript
// host/tm_api/dry_run/
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

* WET RUN - before single test run
```javascript
// host/tm_api/test_start/
let data = {
  "machine_name": "machine #1",
  "file_path": "/virtual_testing_machine/src/test_cases/01_feature_lamp",
  "file_name": "01_01_test_lamp.py",
  "timestamp_start": "2018-12-30 13:01:57.573828"
}
```

* WET RUN - after single test run
```javascript
// host/tm_api/test_stop/
let data = {
  "machine_name": "machine #1",
  "file_path": "/virtual_testing_machine/src/test_cases/01_feature_lamp",
  "file_name": "01_01_test_lamp.py",
  "status": "passed",
  "timestamp_stop": "2018-12-30 13:01:59.622177"
}
```

## URLs

| Path  | View | Name |
| ------------- | ------------- | ------------- |
| **Template views:** |
| /matchine/\<int:pk\> | progress_tracking.views.MachineDetailView | machine-detail-view  |
| /machine/\<int:pk\>/last | progress_tracking.views.MachineLastDataView | machine-last-data-view |
| /machine/run_data/\<int:pk\> | progress_tracking.views.DryRunDataDetailView | dry-run-data-detail-view |
| **REST endpoints:** |
| /tm_api/dry_run/ | tm_api.views.DryRunView | dry-run-input |
| /tm_api/test_start/ | tm_api.views.TestStartView | test-start |
| /tm_api/test_stop/ | tm_api.views.TestStopView | test-stop |
| /tm_api/test/\<int:pk\> | tm_api.views.TestDetailView | test-detail |
| /tm_api/scenario/\<int:pk\> | tm_api.views.ScenarioDetailView | scenario-detail |
| /tm_api/master_scenario/\<int:pk\> | tm_api.views.MasterScenarioDetailView | master-scenario-detail |
| /tm_api/machines/ | tm_api.views.MachineListView | machine-list |
| /tm_api/machine_dry_run_datas/\<int:pk\> | tm_api.views.MachineDryRunDatasListView | machine-dry-run-datas |
| /tm_api/machine_last_data/\<int:pk\>/ | tm_api.views.MachineLastDataView | machine-last-data |
| **REST documentation:** |
| /docs/ | | |
| **User views:** |
| /login/ | django.contrib.auth.views.LoginView | login |
| /logout/ | django.contrib.auth.views.LogoutView | logout |
| /password-reset-complete/ | django.contrib.auth.views.PasswordResetCompleteView | password_reset_complete |
| /password-reset-confirm/\<uidb64\>/\<token\>/ | django.contrib.auth.views.PasswordResetConfirmView | password_reset_confirm |
| /password-reset/ | django.contrib.auth.views.PasswordResetView | password_reset |
| /password-reset/done | django.contrib.auth.views.PasswordResetDoneView password_reset_done |
| **WebSockets:** |
| /ws/machine/\<int:pk\>/last/' | consumers.MachineLastRunConsumer |
| /ws/machine/\<int:pk\>/runs/' | consumers.MachineRunsStatusConsumer |
| /ws/machine/status/' | consumers.MachinesStatusConsumer | 


## How it looks

Last run on given machine (autoupdate)
![db_schema](/docs/img/last_run_autoupdate_view.gif)

Details of given run
![db_schema](/docs/img/run_details_view.gif)


## Lessons learned
* Django
    * Django Channels (WebSockets)
    * REST 
        * serialization
        * pagination
* other
    * Git branching
    * jQuery AJAX
    * WebSockets
    * Continous Integration (TravisCI)
   

## Links
* [JavaScript Cookie - JavaScript API for handling browser cookies](https://github.com/js-cookie/js-cookie)
* [highlight.js - Syntax highlighting for the Web](https://highlightjs.org/)
* [A successful Git branching model - Vincent Driessen blog](https://nvie.com/posts/a-successful-git-branching-model/)
* [Django Channels - Documentation](https://channels.readthedocs.io/en/latest/)
* [Django REST framework - Pagination](https://www.django-rest-framework.org/api-guide/pagination/)
