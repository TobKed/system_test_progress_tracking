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
        machine_id = machine.pk

        serializer_last_data = MachineLastDataSerializer(machine)
        async_to_sync(channel_layer.group_send)(
            f"machine_{machine_id}",
            {"type": "machine_data", "machine_data": serializer_last_data.data}
        )

        async_to_sync(channel_layer.group_send)(
            f"machine_status_change",
            {"type": "machine_id", "machine_id": machine_id}
        )
    except:
        pass
