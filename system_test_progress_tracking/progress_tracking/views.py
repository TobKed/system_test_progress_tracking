from django.shortcuts import render
from django.core.paginator import Paginator
from django.views import View
from django.views.generic import (
    DetailView,
    ListView,
)

from tm_api.models import Machine, DryRunData
from tm_api.pagination import CustomListPageSizePagination


def home(request):
    return render(request, 'progress_tracking/home.html')


class MachineListView(View):
    template_name = "progress_tracking/machine_list.html"
    paginate_by = CustomListPageSizePagination.page_size
    cookie_name = "machineListPageSize"

    def get(self, request):
        paginate_by_cookie = request.COOKIES.get(self.cookie_name, self.paginate_by)
        paginate_by = self.request.GET.get("page_size", paginate_by_cookie)
        params = {
            "count": Machine.objects.all().count(),
            "page_number": self.request.GET.get("page", "1"),
            "page_size": self.request.GET.get("page_size", paginate_by),
        }
        response = render(request, self.template_name, params)
        response.set_cookie(key=self.cookie_name, value=paginate_by)
        return response


class MachineDetailView(DetailView):
    model = Machine
    template_name = "progress_tracking/machine_detail.html"
    context_object_name = 'machine'
    paginate_by = CustomListPageSizePagination.page_size
    cookie_name = "machineDetailPageSize"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        page_size = context.get("page_size")
        response = self.render_to_response(context)
        response.set_cookie(key=self.cookie_name, value=page_size)
        return response

    def get_context_data(self, *args, **kwargs):
        paginate_by_cookie = self.request.COOKIES.get(self.cookie_name, self.paginate_by)
        paginate_by = self.request.GET.get("page_size", paginate_by_cookie)
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
            "page_size": self.request.GET.get("page_size", paginate_by),
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
