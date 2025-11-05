"""
URLs for Community app.
"""

from django.urls import path
from . import views

app_name = 'community'

urlpatterns = [
    path('', views.community_list, name='list'),
    path('<int:pk>/', views.community_detail, name='detail'),
    path('create/', views.community_create, name='create'),
    path('<int:pk>/join/', views.community_join, name='join'),
    path('notifications/', views.notifications, name='notifications'),
]
