from django.urls import path
from .views import ProjectListCreateView, ProjectDetailView, ProjectUpdateCreateView

urlpatterns = [
    path('', ProjectListCreateView.as_view(), name='project-list'),
    path('<int:pk>/', ProjectDetailView.as_view(), name='project-detail'),
    path('updates/', ProjectUpdateCreateView.as_view(), name='add-update'),
]