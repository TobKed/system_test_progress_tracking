from django.shortcuts import render
from django.views.generic.list import ListView

from tm_api.models import Machine


def home(request):
    return render(request, 'progress_tracking/home.html')


class MachineListView(ListView):
    model = Machine
    template_name = "progress_tracking/machine_list.html"
    context_object_name = 'machines'
    paginate_by = 5
