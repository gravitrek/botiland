"""Views for Community app."""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def community_list(request):
    return render(request, 'community/list.html')

def community_detail(request, pk):
    return render(request, 'community/detail.html')

@login_required
def community_create(request):
    return render(request, 'community/create.html')

@login_required
def community_join(request, pk):
    from django.http import JsonResponse
    return JsonResponse({'status': 'success'})

@login_required
def notifications(request):
    return render(request, 'community/notifications.html')
