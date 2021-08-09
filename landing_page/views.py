from django.shortcuts import render
from .forms import SignInForm
from django.contrib.auth import login, authenticate
from django.shortcuts import redirect
from django.forms import ValidationError


def landing_page(request):

    if request.method == 'POST':
        form = SignInForm(request.POST)
        username = request.POST.get('username')
        raw_password = request.POST.get('password')
        user = authenticate(username=username, password=raw_password)
        if user:
            if user.is_active:
                login(request, user)
                return redirect('cryptocurrencies_last_price')
            else:
                state = "Your account is not active, please contact the administrator."
        else:
            state= "Your username and/or password were incorrect."

    else:
        form = SignInForm()
        state = ""

    return render(request, 'landing_page/index.html', {'form': form,'state':state})


def registration_completed(request):

    return render(request, 'landing_page/registration-completed.html')