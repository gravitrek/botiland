"""Views for AI Coach app."""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def ai_coach(request):
    return render(request, 'ai_coach/index.html')

@login_required
def insights(request):
    return render(request, 'ai_coach/insights.html')

@login_required
def reports(request):
    return render(request, 'ai_coach/reports.html')
