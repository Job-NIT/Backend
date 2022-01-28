from rest_framework import status
from .models import Category, Project, ProjectRequest
from .serializers import (
    CategorySerializer, ProjectSerializer, ProjectRequestSerializer
)
from .permissions import (
    IsEmployerOrReadOnly, IsFreelancerOrReadOnly,
    IsEmployer, IsFreelancer, IsProjectOwner
)
from django.shortcuts import get_object_or_404
from rest_framework.generics import (
    ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK, HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST
)


class CategoryListView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class ProjectListView(ListCreateAPIView):
    permission_classes = (IsAuthenticated, IsEmployerOrReadOnly)
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()

    def perform_create(self, serializer):
        employer = self.request.user.employer
        serializer.save(employer=employer)


class ProjectView(RetrieveUpdateDestroyAPIView):
    permission_classes = (
        IsAuthenticated, IsEmployerOrReadOnly, IsProjectOwner
    )
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()


class ProjectRequestView(APIView):
    permission_classes = (IsAuthenticated, IsFreelancerOrReadOnly)

    def get(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        project_requests = project.requests.all()

        requests_serializer = ProjectRequestSerializer(
            project_requests,
            many=True
        )

        return Response(data=requests_serializer.data)

    def post(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        freelancer = request.user.freelancer

        if project.freelancer:
            return Response(status=HTTP_400_BAD_REQUEST)

        if project.requests.all().filter(
            freelancer=freelancer
        ).exists():
            return Response(status=HTTP_400_BAD_REQUEST)

        project_request = ProjectRequest.objects.create(
            project=project,
            freelancer=freelancer
        )
        request_serializer = ProjectRequestSerializer(project_request)

        return Response(data=request_serializer.data)


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


class ProjectRequestAcceptView(APIView):
    permission_classes = (IsAuthenticated, IsEmployer, IsProjectOwner)

    def post(self, request, pk):
        project_request = get_object_or_404(ProjectRequest, pk=pk)
        project = project_request.project

        self.check_object_permissions(request, project)

        project.freelancer = project_request.freelancer
        project.save()

        for item in project.requests.all():
            item.delete()

        return Response()


class EmployerProjectsView(ListAPIView):
    permission_classes = (IsAuthenticated, IsEmployer)
    serializer_class = ProjectSerializer

    def get_queryset(self):
        user = self.request.user

        return Project.objects.filter(employer=user.employer)


class FreelancerProjectsView(ListAPIView):
    permission_classes = (IsAuthenticated, IsFreelancer)
    serializer_class = ProjectSerializer

    def get_queryset(self):
        user = self.request.user

        return Project.objects.filter(freelancer=user.freelancer)
