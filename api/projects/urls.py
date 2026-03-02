from django.urls import path
from .views import TestProjectsView

urlpatterns = [
    path("test/", TestProjectsView.as_view(), name="projects-test"),
]