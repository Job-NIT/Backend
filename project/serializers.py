from .models import Project, ProjectRequest
from rest_framework import serializers


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'
        read_only_fields = ('employer',)


class ProjectRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectRequest
        fields = ('project', 'freelancer', 'time')
        read_only_fields = ('time',)
