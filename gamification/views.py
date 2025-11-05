"""Views for Gamification app."""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def badges(request):
    return render(request, 'gamification/badges.html')

def leaderboard(request):
    return render(request, 'gamification/leaderboard.html')

@login_required
def quests(request):
    return render(request, 'gamification/quests.html')
