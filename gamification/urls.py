"""
URLs for Gamification app.
"""

from django.urls import path
from . import views

app_name = 'gamification'

urlpatterns = [
    path('badges/', views.badges, name='badges'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('quests/', views.quests, name='quests'),
]
