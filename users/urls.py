"""
URLs for Users app.
"""

from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path('<int:pk>/', views.user_detail, name='detail'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
