from rest_framework import status
from .models import Project, ProjectRequest
from .serializers import ProjectSerializer, ProjectRequestSerializer
from .permissions import IsEmployer, IsFreelancer
from django.shortcuts import get_object_or_404
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK, HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST
)


class ProjectListView(ListCreateAPIView):
    permission_classes = (IsAuthenticated, IsEmployer)
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()

    def perform_create(self, serializer):
        employer = self.request.user.employer
        serializer.save(employer=employer)


class ProjectRequestView(APIView):
    permission_classes = (IsAuthenticated, IsFreelancer)

    def get(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        project_requests = project.requests.all()

        requests_serializer = ProjectRequestSerializer(
            project_requests,
            many=True
        )

        return Response(data=requests_serializer.data, status=HTTP_200_OK)

    def post(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        freelancer = request.user.freelancer

        if project.requests.all().filter(
            freelancer=freelancer
        ).exists():
            return Response(status=HTTP_400_BAD_REQUEST)

        project_request = ProjectRequest.objects.create(
            project=project,
            freelancer=freelancer
        )
        request_serializer = ProjectRequestSerializer(project_request)

        return Response(data=request_serializer.data, status=HTTP_200_OK)


class ProjectRequestRemoveView(APIView):
    permission_classes = (IsAuthenticated, IsFreelancer)

    def post(self, request, pk):
        freelancer = request.user.freelancer
        project = get_object_or_404(Project, pk=pk)

        project_request = ProjectRequest.objects.filter(
            project=project,
            freelancer=freelancer
        )

        if not project_request.exists():
            return Response(status=HTTP_400_BAD_REQUEST)

        project_request[0].delete()

        return Response(status=HTTP_204_NO_CONTENT)
