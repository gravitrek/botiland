"""
URLs for Analytics app.
"""

from django.urls import path
from . import views

app_name = 'analytics'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('goals/<int:goal_id>/', views.goal_analytics, name='goal'),
]
