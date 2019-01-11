from django.shortcuts import render
from django.core.paginator import Paginator
from django.views import View
from django.views.generic import (
    DetailView,
    ListView,
)

from tm_api.models import Machine, DryRunData
from tm_api.pagination import MachineListPagePagination


def home(request):
    return render(request, 'progress_tracking/home.html')


class MachineListView(View):
    template_name = "progress_tracking/machine_list.html"
    paginate_by = MachineListPagePagination.page_size

    def get(self, request):
        params = {
            "count": Machine.objects.all().count(),
            "page_number": self.request.GET.get("page", "1"),
            "page_size": self.request.GET.get("page_size", self.paginate_by),
        }
        return render(request, self.template_name, params)


class MachineDetailView(DetailView):
    model = Machine
    template_name = "progress_tracking/machine_detail.html"
    context_object_name = 'machine'
    paginate_by = MachineListPagePagination.page_size

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        dry_run_datas = self.object.dry_run_datas.all()
        paginator = Paginator(dry_run_datas, self.paginate_by)
        page_obj = paginator.page(self.request.GET.get("page", 1))
        is_paginated = page_obj.has_other_pages()
        extra_context = {
            "dry_run_datas": page_obj,
            "page_obj": page_obj,
            "is_paginated": is_paginated,

            "count": self.object.dry_run_datas.all().count(),
            "page_number": self.request.GET.get("page", "1"),
            "page_size": self.request.GET.get("page_size", self.paginate_by),
        }
        context_data.update(extra_context)
        return context_data


class DryRunDataDetailView(DetailView):
    model = DryRunData
    template_name = "progress_tracking/dry_run_data_detail.html"
    context_object_name = 'dry_run_data'


class MachineLastDataView(DetailView):
    model = Machine
    template_name = "progress_tracking/machine_last_data.html"
    context_object_name = 'machine'
