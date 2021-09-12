from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from landing_page.views import LOGIN_URL
from algo_trade.ETF_intelligent_portfolio import temp
from .forms import SectorForm
from api.models import ETF

@login_required(login_url=LOGIN_URL)
def algorithmic_trading_page(request):
    context = {}
    return render(request, 'algo_trade/algorithmic_trading_page.html', context)

@login_required(login_url=LOGIN_URL)
def sector_page(request):
    if request.method == 'POST':
        form = SectorForm(request.POST)
        if form.is_valid():
            sectors = form.cleaned_data.get('sectors')
            request.session['sectors'] = sectors
            return redirect('etf_selection_page')
    else:
        form = SectorForm ()
    context = {'form': form}
    return render(request, 'algo_trade/sector_page.html', context)

@login_required(login_url=LOGIN_URL)
def etf_selection_page(request):
    sectors = request.session.get('sectors')
    list_of_etfs = ETF.objects.filter(sector__in=sectors)
    if request.method == 'POST':
            etfs = request.POST.getlist('etfs')
            request.session['etfs'] = etfs
            return redirect('etf_input_page')
    context = {'etfs': list_of_etfs,
               'sectors': sectors,
               }

    return render(request, 'algo_trade/etf_selection_page.html', context)

@login_required(login_url=LOGIN_URL)
def etf_input_page(request):
    etfs = request.session.get('etfs')
    context = {'etfs':etfs}
    return render(request, 'algo_trade/etf_input_page.html', context)

@login_required(login_url=LOGIN_URL)
def etf_result_page(request):
    uri = temp()
    context = {'data': uri}
    return render(request, 'algo_trade/etf_result_page.html', context)

