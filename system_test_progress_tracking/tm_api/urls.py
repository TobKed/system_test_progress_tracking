from django.urls import path
from .views import DryRunView, TestStartView

urlpatterns = [
    path('dry_run/', DryRunView.as_view()),
    path('test_start/', TestStartView.as_view()),
    # path('test_stop/', ,
]
