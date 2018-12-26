from django.shortcuts import render
from django.core.paginator import Paginator
from django.views.generic import (
    DetailView,
    ListView,
)

from tm_api.models import Machine, DryRunData


def home(request):
    return render(request, 'progress_tracking/home.html')


class MachineListView(ListView):
    model = Machine
    template_name = "progress_tracking/machine_list.html"
    context_object_name = 'machines'
    paginate_by = 5


class MachineDetailView(DetailView):
    model = Machine
    template_name = "progress_tracking/machine_detail.html"
    context_object_name = 'machine'
    paginate_by = 5

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        dry_run_datas = self.object.dry_run_datas.all()
        paginator = Paginator(dry_run_datas, self.paginate_by)
        page_obj = paginator.page(self.request.GET.get("page", 1))
        is_paginated = True if dry_run_datas else False
        extra_context = {
            "dry_run_datas": page_obj,
            "page_obj": page_obj,
            "is_paginated": is_paginated,
        }
        context_data.update(extra_context)
        return context_data


class DryRunDataDetailView(DetailView):
    model = DryRunData
    template_name = "progress_tracking/dry_run_data_detail.html"
    context_object_name = 'dry_run_data'
