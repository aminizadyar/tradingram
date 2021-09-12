from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from landing_page.views import LOGIN_URL


@login_required(login_url=LOGIN_URL)
def algorithmic_trading_page(request):
    context = {'qs': "qs"}
    return render(request, 'algo_trade/algorithmic_trading_page.html', context)

