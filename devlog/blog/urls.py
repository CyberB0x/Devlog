from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('article/<int:pk>/', views.article_detail, name='article_detail'),
    path('article/add/', views.add_article, name='add_article'),
    path('article/<int:pk>/delete/', views.delete_article, name='delete_article'),
    path('profile/', views.profile, name='profile'),
    path('register/', views.register, name='register'),
    path('api/views/<int:pk>/', views.stats_view, name='article_stats'),
]
