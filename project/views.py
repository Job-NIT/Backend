from .models import Project
from .serializers import ProjectSerializer
from .permissions import IsEmployer
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated


class ProjectListView(ListCreateAPIView):
    permission_classes = (IsAuthenticated, IsEmployer)
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()

    def perform_create(self, serializer):
        employer = self.request.user.employer
        serializer.save(employer=employer)
