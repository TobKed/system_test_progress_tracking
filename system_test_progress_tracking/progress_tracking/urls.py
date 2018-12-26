from django.urls import path
from .views import (
    home,
    MachineDetailView,
    MachineListView
)


urlpatterns = [
    # path('', home,  name='home-view'),
    path('', MachineListView.as_view(),  name='home-view'),
    path('machine/', MachineListView.as_view(),  name='machine-list-view'),
    path('machine/<int:pk>', MachineDetailView.as_view(),  name='machine-detail-view'),
]
