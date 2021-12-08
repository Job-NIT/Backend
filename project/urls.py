from .views import (
    ProjectListView, ProjectRequestView, ProjectRequestRemoveView
)
from django.urls import path


urlpatterns = [
    path('list/', ProjectListView.as_view()),
    path('<int:pk>/request/', ProjectRequestView.as_view()),
    path('<int:pk>/request/remove/', ProjectRequestRemoveView.as_view())
]
