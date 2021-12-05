from user.models import User
from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsEmployer(BasePermission):
    def has_permission(self, request, view):
        return bool(
            (request.method in SAFE_METHODS) or
            (request.user.user_type == User.USER_TYPE.EMPLOYER)
        )


class IsFreelancer(BasePermission):
    def has_permission(self, request, view):
        return bool(
            (request.method in SAFE_METHODS) or
            (request.user.user_type == User.USER_TYPE.FREELANCER)
        )
