# Virtual System Testing Machine

## Scripts execution hierarchy (simplified functions)
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

## Used REST endpoints:

| Path  | View | Name |
| ------------- | ------------- | ------------- |
| /tm_api/dry_run/ | tm_api.views.DryRunView |
| /tm_api/test_start/ | tm_api.views.TestStartView |
| /tm_api/test_stop/ | tm_api.views.TestStopView |