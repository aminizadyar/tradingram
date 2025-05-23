from django.shortcuts import render
from .forms import UserForm
from .forms import ProfileForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib import messages



@login_required
@transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST,request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, ('Your profile was successfully updated!'))
            return redirect('cryptocurrencies_last_price')
        else:
            messages.error(request, ('Please correct the error below.'))
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'social_media/update_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })
