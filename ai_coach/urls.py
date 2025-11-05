"""
URLs for AI Coach app.
"""

from django.urls import path
from . import views

app_name = 'ai_coach'

urlpatterns = [
    path('', views.ai_coach, name='index'),
    path('insights/', views.insights, name='insights'),
    path('reports/', views.reports, name='reports'),
]
