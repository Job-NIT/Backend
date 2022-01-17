from .models import User, Freelancer, Employer
from .serializers import (
    FreelancerSerializer, EmployerSerializer, UserProfileImageSerializer
)
from .utils.users import get_user_serializer, get_user_profile_serializer
from .permissions import IsUserProfileOrReadOnly
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.generics import (
    CreateAPIView, RetrieveAPIView, RetrieveUpdateAPIView, UpdateAPIView
)
from django.shortcuts import get_object_or_404


class FreelancerRegisterView(CreateAPIView):
    serializer_class = FreelancerSerializer
    queryset = Freelancer.objects.all()


class EmployerRegisterView(CreateAPIView):
    serializer_class = EmployerSerializer
    queryset = Employer.objects.all()


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        request.auth.delete()

        return Response(status=HTTP_204_NO_CONTENT)


class UserInfoView(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user

    def get_serializer(self, user, *args, **kwargs):
        serializer_class, instance = get_user_serializer(user)
        kwargs.setdefault('context', self.get_serializer_context())
        return serializer_class(instance, *args, **kwargs)


class UserProfileView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated, IsUserProfileOrReadOnly)
    queryset = User.objects.all()

    def get_object(self):
        if self.request.method == 'GET':
            pk = self.kwargs.get('pk')
            return get_object_or_404(User, pk=pk)

        elif self.request.method in ['PATCH', 'PUT']:
            return self.request.user

    def get_serializer(self, user, *args, **kwargs):
        serializer_class, instance = get_user_profile_serializer(user)

        kwargs.setdefault('context', self.get_serializer_context())
        return serializer_class(instance, *args, **kwargs)


class UserProfileImageView(UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserProfileImageSerializer

    def get_object(self):
        return self.request.user
