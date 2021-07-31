from django.shortcuts import render


def dashboard(request):
    return render(request, 'paper_trade/dashboard.html')
