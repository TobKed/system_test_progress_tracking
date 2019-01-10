from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from .models import (
    Test,
    Scenario,
    MasterScenario,
    DryRunData,
    Machine,
    WAITING,
    RUNNING
)

from .serializers import (
    DryRunDataSerializer,
    TestStartSerializer,
    TestStopSerializer,
    TestModelSerializer,
    ScenarioModelSerializer,
    MasterScenarioModelSerializer,
    MasterScenarioModelDetailSerializer,
    MachineLastDataSerializer,
    MachineListSerializer,
    MachineDryRunDatasSerializer,
)

from .pagination import MachineListPagePagination


class DryRunView(APIView):
    def post(self, request, format=None):
        serializer = DryRunDataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TestStartView(APIView):
    def post(self, request, format=None):
        serializer = TestStartSerializer(data=request.data)
        if serializer.is_valid():
            machine_name = serializer.validated_data.get("machine_name")
            timestamp_start = serializer.validated_data.get("timestamp_start")
            file_name = serializer.validated_data.get("file_name")
            file_path = serializer.validated_data.get("file_path")
            machine = Machine.objects.get(machine_name__iexact=machine_name)
            first_waiting_test = machine.get_tests(file_name=file_name, file_path=file_path,
                                                   status=WAITING).first() if machine else None
            if first_waiting_test:
                first_waiting_test.status = "running"
                first_waiting_test.timestamp_start = timestamp_start
                first_waiting_test.save()
                return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TestStopView(APIView):
    def post(self, request, format=None):
        serializer = TestStopSerializer(data=request.data)
        if serializer.is_valid():
            machine_name= serializer.validated_data.get("machine_name")
            timestamp_stop = serializer.validated_data.get("timestamp_stop")
            status_ = serializer.validated_data.get("status")
            file_name = serializer.validated_data.get("file_name")
            file_path = serializer.validated_data.get("file_path")
            machine = Machine.objects.get(machine_name__iexact=machine_name)
            first_running_test = machine.get_tests(file_name=file_name, file_path=file_path,
                                                   status=RUNNING).first() if machine else None
            if first_running_test:
                first_running_test.status = status_
                first_running_test.timestamp_stop = timestamp_stop
                first_running_test.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TestDetailView(APIView):
    def get(self, request, pk, format=None):
        obj = get_object_or_404(Test, pk=pk)
        serializer = TestModelSerializer(obj, context={"request": request})
        return Response(serializer.data)


class ScenarioDetailView(APIView):
    def get(self, request, pk, format=None):
        obj = get_object_or_404(Scenario, pk=pk)
        serializer = ScenarioModelSerializer(obj, context={"request": request})
        return Response(serializer.data)


class MasterScenarioDetailView(APIView):
    def get(self, request, pk, format=None):
        obj = get_object_or_404(MasterScenario, pk=pk)
        serializer = MasterScenarioModelSerializer(obj, context={"request": request})
        return Response(serializer.data)


class MasterScenarioDetailFullView(APIView):
    def get(self, request, pk, format=None):
        obj = get_object_or_404(MasterScenario, pk=pk)
        serializer = MasterScenarioModelDetailSerializer(obj, context={"request": request})
        return Response(serializer.data)


class MachineLastDataView(APIView):
    def get(self, request, pk, format=None):
        obj = get_object_or_404(Machine, pk=pk)
        serializer = MachineLastDataSerializer(obj, context={"request": request})
        return Response(serializer.data)


class MachineListView(generics.ListAPIView):
    queryset = Machine.objects.all()
    serializer_class = MachineListSerializer
    pagination_class = MachineListPagePagination


class MachineDryRunDatasListView(generics.ListAPIView):
    queryset = DryRunData.objects.all()
    serializer_class = MachineDryRunDatasSerializer
    pagination_class = MachineListPagePagination
    lookup_url_kwarg = "pk"

    def get_queryset(self, *args, **kwargs):
        pk = self.kwargs.get(self.lookup_url_kwarg)
        return DryRunData.objects.filter(machine_id=pk)
