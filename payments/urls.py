from django.urls import path
from . import views

urlpatterns = [
    path('initiate-payment/<int:project_id>/', views.initiate_stk_push, name='initiate_payment'),
    path('callback/', views.mpesa_callback, name='mpesa_callback'),
]