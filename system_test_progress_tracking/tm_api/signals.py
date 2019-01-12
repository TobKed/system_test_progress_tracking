from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import MasterScenario
from .serializers import MachineLastDataSerializer


channel_layer = get_channel_layer()


@receiver(post_save, sender=MasterScenario)
def send_message_to_channels(sender, instance, **kwargs):
    try:
        machine = instance.dryrundata.machine
        dry_run_data = instance.dryrundata
        machine_id = machine.pk

        # routing:
        # path('ws/machine/<int:pk>/last/', consumers.MachineLastRunConsumer)
        serializer_last_data = MachineLastDataSerializer(machine)
        async_to_sync(channel_layer.group_send)(
            f"machine_last_data_{machine_id}",
            {"type": "machine_data", "machine_data": serializer_last_data.data}
        )

        # routing:
        # path('ws/machine/status/', consumers.MachinesStatusConsumer),
        async_to_sync(channel_layer.group_send)(
            f"machine_status_change",
            {"type": "machine_id_status",
             "machine_id_status": {
                    "id": machine_id,
                    "status": machine.get_last_master_scenario_status()
                }
             }
        )

        # routing
        # path('ws/machine/<int:pk>/runs/', consumers.MachineRunsStatusConsumer),
        async_to_sync(channel_layer.group_send)(
            f"machine_runs_data_{machine_id}",
            {"type": "run_data",
             "run_data": {
                    "id": dry_run_data.pk,
                    "status": dry_run_data.master_scenario.status,
                }
             }
        )

    except:
        pass
