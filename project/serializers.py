from .models import Project, ProjectRequest
from user.serializers import UserDetailSerializer
from rest_framework import serializers


class ProjectSerializer(serializers.ModelSerializer):
    employer = UserDetailSerializer(source="employer.user", read_only=True)

    class Meta:
        model = Project
        fields = '__all__'


class ProjectRequestSerializer(serializers.ModelSerializer):
    freelancer = UserDetailSerializer(source="freelancer.user", read_only=True)

    class Meta:
        model = ProjectRequest
        fields = ('id', 'project', 'freelancer', 'time')
        read_only_fields = ('time',)
