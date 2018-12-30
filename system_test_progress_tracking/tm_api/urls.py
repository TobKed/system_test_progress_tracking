from django.urls import path
from .views import (
    DryRunView,
    TestStartView,
    TestStopView,
    TestDetailView,
    ScenarioDetailView,
    MasterScenarioDetailView,
)

urlpatterns = [
    path('dry_run/', DryRunView.as_view()),
    path('test_start/', TestStartView.as_view()),
    path('test_stop/', TestStopView.as_view()),

    path('test/<int:pk>', TestDetailView.as_view()),
    path('scenario/<int:pk>', ScenarioDetailView.as_view()),
    path('master_scenario/<int:pk>', MasterScenarioDetailView.as_view()),
]
