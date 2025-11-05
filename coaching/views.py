"""Views for Coaching app."""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def coach_list(request):
    return render(request, 'coaching/list.html')

def coach_detail(request, pk):
    return render(request, 'coaching/detail.html')

@login_required
def book_session(request, coach_id):
    return render(request, 'coaching/book.html')

@login_required
def my_sessions(request):
    return render(request, 'coaching/sessions.html')
