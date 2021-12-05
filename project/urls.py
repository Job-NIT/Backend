from .views import ProjectListView
from django.urls import path


urlpatterns = [
    path('list/', ProjectListView.as_view())
]
