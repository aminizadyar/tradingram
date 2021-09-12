from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from landing_page.views import LOGIN_URL
from algo_trade.ETF_intelligent_portfolio import temp

@login_required(login_url=LOGIN_URL)
def algorithmic_trading_page(request):
    context = {}
    return render(request, 'algo_trade/algorithmic_trading_page.html', context)

@login_required(login_url=LOGIN_URL)
def etf_optimizer_page(request):
    uri = temp()
    context = {'data': uri}
    return render(request, 'algo_trade/etf_optimizer_page.html', context)

