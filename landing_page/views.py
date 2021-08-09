from django.shortcuts import render
from .forms import SignUpForm
from .forms import SignInForm
from django.contrib.auth import login, authenticate
from django.shortcuts import redirect



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


def signup(request):
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
    return render(request, 'landing_page/signup.html',{'form':form})