from user.models import User
from user.serializers import (
    FreelancerSerializer, EmployerSerializer,
    FreelancerProfileSerializer, EmployerProfileSerializer,
)

def get_user_serializer(user):
    if user.user_type == User.USER_TYPE.FREELANCER:
        serializer_class = FreelancerSerializer
        instance = user.freelancer

    elif user.user_type == User.USER_TYPE.EMPLOYER:
        serializer_class = EmployerSerializer
        instance = user.employer

    return serializer_class, instance


def get_user_profile_serializer(user):
    if user.user_type == User.USER_TYPE.FREELANCER:
        serializer_class = FreelancerProfileSerializer
        instance = user.freelancer

    elif user.user_type == User.USER_TYPE.EMPLOYER:
        serializer_class = EmployerProfileSerializer
        instance = user.employer

    return serializer_class, instance
