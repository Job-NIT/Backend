from .models import Category, Project, ProjectRequest
from user.serializers import UserDetailSerializer
from rest_framework import serializers
from django.shortcuts import get_object_or_404


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProjectSerializer(serializers.ModelSerializer):
    employer = UserDetailSerializer(source="employer.user", read_only=True)
    freelancer = UserDetailSerializer(source="freelancer.user", read_only=True)
    category = CategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = Project
        fields = '__all__'

    def create(self, validated_data):
        category_id = validated_data.pop('category_id', None)

        if category_id:
            category = get_object_or_404(Category, pk=category_id)
            validated_data['category'] = category

        return super().create(validated_data)


class ProjectRequestSerializer(serializers.ModelSerializer):
    freelancer = UserDetailSerializer(source="freelancer.user", read_only=True)

    class Meta:
        model = ProjectRequest
        fields = ('id', 'project', 'freelancer', 'created_at')
        read_only_fields = ('time',)
