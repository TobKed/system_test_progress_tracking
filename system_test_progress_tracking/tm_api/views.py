from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Test, DryRunData, Machine, WAITING

from .serializers import DryRunDataSerializer, TestStartSerializer


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
            file_name = serializer.validated_data.get("file_name")
            file_path = serializer.validated_data.get("file_path")
            machine = Machine.objects.get(machine_name__iexact=machine_name)
            first_waiting_test = machine.get_tests(file_name=file_name, file_path=file_path,
                                                   status=WAITING).first() if machine else None
            if first_waiting_test:
                first_waiting_test.status = "running"
                first_waiting_test.save()
                return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


