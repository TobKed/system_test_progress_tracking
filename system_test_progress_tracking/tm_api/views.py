from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Test, DryRunData, Machine, WAITING, RUNNING

from .serializers import DryRunDataSerializer, TestStartSerializer, TestStopSerializer


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
