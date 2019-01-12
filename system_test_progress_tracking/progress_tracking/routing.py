from django.urls import path

from . import consumers


websocket_urlpatterns = [
    path('ws/machine/<int:pk>/last/', consumers.MachineLastRunConsumer),
    path('ws/machine/status/', consumers.MachinesStatusConsumer),
]
