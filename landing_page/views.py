from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import RegistrationForm
from .models import User

def landing_page(request):

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            obj = User()
            obj.username = form.cleaned_data['username']
            obj.email = form.cleaned_data['email']
            obj.password = form.cleaned_data['password']
            obj.save()
            return HttpResponseRedirect('/registration-completed')
    else:
        form = RegistrationForm()


    return render(request, 'landing_page/index.html', {'form': form})


def registration_completed(request):

    return render(request, 'landing_page/registration-completed.html')