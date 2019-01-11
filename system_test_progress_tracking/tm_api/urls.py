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
    path('dry_run/', DryRunView.as_view()),
    path('test_start/', TestStartView.as_view()),
    path('test_stop/', TestStopView.as_view()),

    path('test/<int:pk>', TestDetailView.as_view()),
    path('scenario/<int:pk>', ScenarioDetailView.as_view()),
    path('master_scenario/<int:pk>', MasterScenarioDetailView.as_view()),
    path('master_scenario_full/<int:pk>', MasterScenarioDetailFullView.as_view()),

    path('machine_last_data/<int:pk>/', MachineLastDataView.as_view()),
    path('machines/', MachineListView.as_view()),
    path('machine_dry_run_datas/<int:pk>', MachineDryRunDatasListView.as_view()),
]
