from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Test, DryRunData, Machine

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
            machine_tests = machine.get_tests(file_name=file_name, file_path=file_path)
            last_test = machine_tests.first()
            last_test.status = "running"
            last_test.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


