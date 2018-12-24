from django.urls import path
from .views import (
    home,
    MachineListView
)


urlpatterns = [
    path('', home,  name='home-view'),
    path('machine/', MachineListView.as_view(),  name='machine-list-view'),
]
