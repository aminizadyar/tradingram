from django.shortcuts import render
from .forms import SignUpForm
from django.contrib.auth import login, authenticate
from django.shortcuts import redirect


def landing_page(request):

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('cryptocurrencies_last_price')
    else:
        form = SignUpForm()

    return render(request, 'landing_page/index.html', {'form': form})


def registration_completed(request):

    return render(request, 'landing_page/registration-completed.html')