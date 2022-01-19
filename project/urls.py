from .views import (
    CategoryListView, ProjectListView, ProjectView,
    ProjectRequestView, ProjectRequestRemoveView
)
from django.urls import path


urlpatterns = [
    path('categories/', CategoryListView.as_view()),
    path('list/', ProjectListView.as_view()),
    path('<int:pk>/', ProjectView.as_view()),
    path('<int:pk>/request/', ProjectRequestView.as_view()),
    path('<int:pk>/request/remove/', ProjectRequestRemoveView.as_view())
]
