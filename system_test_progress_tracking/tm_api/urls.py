from django.urls import path
from .views import DryRunView, TestStartView, TestStopView

urlpatterns = [
    path('dry_run/', DryRunView.as_view()),
    path('test_start/', TestStartView.as_view()),
    path('test_stop/', TestStopView.as_view()),
]
