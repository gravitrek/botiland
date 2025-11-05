"""Views for Analytics app."""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    return render(request, 'analytics/dashboard.html')

@login_required
def goal_analytics(request, goal_id):
    return render(request, 'analytics/goal.html')
