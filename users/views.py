"""Views for Users app."""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def profile(request):
    return render(request, 'users/profile.html')

@login_required
def profile_edit(request):
    return render(request, 'users/profile_edit.html')

def user_detail(request, pk):
    return render(request, 'users/detail.html')

@login_required
def dashboard(request):
    return render(request, 'users/dashboard.html')
