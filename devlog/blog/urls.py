from django.urls import path
from .views import toggle_like, upload_image
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('article/<int:pk>/', views.article_detail, name='article_detail'),
    path('article/add/', views.add_article, name='add_article'),
    path('article/<int:pk>/delete/', views.delete_article, name='delete_article'),
    path('api/views/<int:pk>/', views.stats_view, name='article_stats'),
    path('like/<int:pk>/', toggle_like, name='toggle_like'),
    path('stats/<int:pk>/', views.stats_view, name='stats_view'),
    path('upload/image/', upload_image, name='upload_image'),
    path('search/', views.search_articles, name='search_articles'),

]
