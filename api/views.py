from django.shortcuts import render
from .models import Symbol

def markets_page(request):
    qs = Symbol.objects.all()
    context = {'qs': qs}
    return render(request, 'api/markets_page.html', context)
