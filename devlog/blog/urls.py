from django.urls import path
from .views import toggle_like, upload_image
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('article/<int:pk>/', views.article_detail, name='article_detail'),
    path('article/add/', views.add_article, name='add_article'),
    path('article/<int:pk>/delete/', views.delete_article, name='delete_article'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('register/', views.register, name='register'),
    path('api/views/<int:pk>/', views.stats_view, name='article_stats'),
    path('like/<int:pk>/', toggle_like, name='toggle_like'),
    path('stats/<int:pk>/', views.stats_view, name='stats_view'),
    path('upload_images/', upload_image, name='upload_image'),

]
