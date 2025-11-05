"""Views for Payments app."""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

@login_required
def buy_credits(request):
    return render(request, 'payments/buy_credits.html')

@login_required
def subscribe(request):
    return render(request, 'payments/subscribe.html')

@login_required
def transactions(request):
    return render(request, 'payments/transactions.html')

@csrf_exempt
def stripe_webhook(request):
    return JsonResponse({'status': 'success'})
