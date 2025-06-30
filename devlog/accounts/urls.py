from django.urls import path
from . import views

urlpatterns = [
    path('forgot/', views.forgot_password, name='forgot_password'),
    path('verify/', views.verify_code, name='verify_code'),
    path('reset/', views.reset_password, name='reset_password'),

]