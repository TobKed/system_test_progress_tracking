from django.urls import path
from .views import DryRunView

urlpatterns = [
    path('dry_run/', DryRunView.as_view()),
    # path('test_start/', ,
    # path('test_stop/', ,
]
