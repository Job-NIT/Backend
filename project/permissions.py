from user.models import User
from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsEmployerOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return bool(
            (request.method in SAFE_METHODS) or
            (request.user.user_type == User.USER_TYPE.EMPLOYER)
        )


class IsFreelancerOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return bool(
            (request.method in SAFE_METHODS) or
            (request.user.user_type == User.USER_TYPE.FREELANCER)
        )


class IsEmployer(BasePermission):
    def has_permission(self, request, view):
        return (request.user.user_type == User.USER_TYPE.EMPLOYER)


class IsFreelancer(BasePermission):
    def has_permission(self, request, view):
        return (request.user.user_type == User.USER_TYPE.FREELANCER)


class IsProjectOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(
            (request.method in SAFE_METHODS) or
            (obj.employer == request.user.employer)
        )
