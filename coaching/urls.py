"""
URLs for Coaching app.
"""

from django.urls import path
from . import views

app_name = 'coaching'

urlpatterns = [
    path('', views.coach_list, name='list'),
    path('<int:pk>/', views.coach_detail, name='detail'),
    path('<int:coach_id>/book/', views.book_session, name='book_session'),
    path('sessions/', views.my_sessions, name='my_sessions'),
]
