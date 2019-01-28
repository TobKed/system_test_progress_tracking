from django.urls import path
from .views import (
    DryRunView,
    TestStartView,
    TestStopView,
    TestDetailView,
    ScenarioDetailView,
    MasterScenarioDetailView,
    MasterScenarioDetailFullView,
    MachineLastDataView,
    MachineListView,
    MachineDryRunDatasListView,
)

urlpatterns = [
    path('dry_run/', DryRunView.as_view(), name='dry-run-input'),
    path('test_start/', TestStartView.as_view(), name='test-start'),
    path('test_stop/', TestStopView.as_view(), name='test-stop'),

    path('test/<int:pk>', TestDetailView.as_view(), name='test-detail'),
    path('scenario/<int:pk>', ScenarioDetailView.as_view(), name='scenario-detail'),
    path('master_scenario/<int:pk>', MasterScenarioDetailView.as_view(), name='master-scenario-detail'),
    path('master_scenario_full/<int:pk>', MasterScenarioDetailFullView.as_view(), name='master-scenario-detail-full'),

    path('machine_last_data/<int:pk>/', MachineLastDataView.as_view(), name='machine-last-data'),
    path('machines/', MachineListView.as_view(), name='machine-list'),
    path('machine_dry_run_datas/<int:pk>', MachineDryRunDatasListView.as_view(), name='machine-dry-run-datas'),
]
