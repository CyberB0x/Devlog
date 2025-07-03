from django.urls import path
from . import views
from .views import login_view

urlpatterns = [
    path('send-verification-email/', views.send_verification_email, name='send_verification_email'),
    path('forgot/', views.forgot_password, name='forgot_password'),
    path('verify/', views.verify_code, name='verify_code'),
    path('reset/', views.reset_password, name='reset_password'),
    path('login/', login_view, name='login'),
    path('send-email-code/', views.send_verification_email, name='send_email_code'),
    path('verify-email/', views.verify_email, name='verify_email'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile_view, name='profile'),
]
