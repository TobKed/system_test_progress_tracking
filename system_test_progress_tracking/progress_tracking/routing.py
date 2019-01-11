from django.urls import path

from . import consumers


websocket_urlpatterns = [
    path('ws/machine/<int:pk>/last/', consumers.MachineConsumer),
    path('ws/machine/status/', consumers.MachineStatusConsumer),
]
