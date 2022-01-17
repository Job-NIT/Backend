from .views import (
    FreelancerRegisterView, EmployerRegisterView, LogoutView,
    UserInfoView, UserProfileView, UserProfileImageView
)
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token


app_name = 'user'

urlpatterns = [
    path('register/freelancer/', FreelancerRegisterView.as_view()),
    path('register/employer/', EmployerRegisterView.as_view()),
    path('login/', obtain_auth_token, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('user-info/', UserInfoView.as_view(), name='user-info'),
    path(
        'profile/', UserProfileView.as_view(http_method_names=['patch', 'put'])
    ),
    path(
        'profile/<int:pk>/', UserProfileView.as_view(http_method_names=['get'])
    ),
    path('profile-image/', UserProfileImageView.as_view())
]
