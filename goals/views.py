"""
Views for Goals app.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Goal, Milestone, Action


@login_required
def goal_list(request):
    goals = Goal.objects.filter(user=request.user)
    return render(request, 'goals/list.html', {'goals': goals})


@login_required
def goal_create(request):
    return render(request, 'goals/create.html')


@login_required
def goal_detail(request, pk):
    goal = get_object_or_404(Goal, pk=pk)
    return render(request, 'goals/detail.html', {'goal': goal})


@login_required
def goal_edit(request, pk):
    goal = get_object_or_404(Goal, pk=pk, user=request.user)
    return render(request, 'goals/edit.html', {'goal': goal})


@login_required
def goal_delete(request, pk):
    goal = get_object_or_404(Goal, pk=pk, user=request.user)
    if request.method == 'POST':
        goal.delete()
        return redirect('goals:list')
    return render(request, 'goals/delete.html', {'goal': goal})


@login_required
def goal_replicate(request, pk):
    return JsonResponse({'status': 'success'})


def template_marketplace(request):
    templates = Goal.objects.filter(is_template=True, privacy='public')
    return render(request, 'goals/templates.html', {'templates': templates})


@login_required
def milestone_create(request, goal_pk):
    return JsonResponse({'status': 'success'})


@login_required
def milestone_complete(request, pk):
    milestone = get_object_or_404(Milestone, pk=pk)
    milestone.mark_complete()
    return JsonResponse({'status': 'success'})


@login_required
def action_create(request, milestone_pk):
    return JsonResponse({'status': 'success'})


@login_required
def action_complete(request, pk):
    action = get_object_or_404(Action, pk=pk)
    action.mark_complete_today()
    return JsonResponse({'status': 'success'})
