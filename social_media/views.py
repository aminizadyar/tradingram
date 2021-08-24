from django.shortcuts import render
from .forms import UserForm, ProfileForm, PostForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib import messages
from django.http import HttpResponseRedirect
from .models import Post, UserFollow
from paper_trade.models import OrderOpenPosition
from django.contrib.auth.models import User
import datetime
from landing_page.views import LOGIN_URL


@login_required(login_url=LOGIN_URL)
def user_profile_page(request,username):
    viewed_user=User.objects.get(username__iexact=username)
    viewing_user = request.user
    is_followed = False
    if UserFollow.objects.filter(following_user = viewing_user , followed_user =viewed_user).exists():
        is_followed = True
    if request.method == 'POST':
        post_form = PostForm(request.POST)
        if post_form.is_valid():
            post_obj = Post()
            post_obj.user = request.user
            post_obj.text_content = post_form.cleaned_data['text_content']
            post_obj.save()
            messages.success(request, ('Your post was successfully published!'))
            return redirect('user_profile_page',username=request.user.username)
        else:
            messages.error(request, ('Please correct the error below.'))
    else:
        post_form = PostForm()
    return render(request, 'social_media/user_profile_page.html', {
        'viewed_user': viewed_user,
        'viewing_user': viewing_user,
        'is_followed': is_followed,
        'post_form': post_form,
    })


@login_required(login_url=LOGIN_URL)
@transaction.atomic
def update_profile_page(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST,request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, ('Your profile was successfully updated!'))
            return redirect('user_profile_page',username=request.user.username)
        else:
            messages.error(request, ('Please correct the error below.'))
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'social_media/update_profile_page.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


def like_logic(request,post_id):
    related_post = Post.objects.get(id=post_id)
    related_post.likes.add(request.user)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def unlike_logic(request,post_id):
    related_post = Post.objects.get(id=post_id)
    related_post.likes.remove(request.user)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def follow_logic(request,followed_user_username):
    followed_user = User.objects.get(username__iexact=followed_user_username)
    new_follow = UserFollow()
    new_follow.followed_user = followed_user
    new_follow.following_user = request.user
    new_follow.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def unfollow_logic(request, followed_user_username):
    followed_user = User.objects.get(username__iexact=followed_user_username)
    UserFollow.objects.filter(following_user = request.user , followed_user = followed_user).delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url=LOGIN_URL)
def feed_page(request):
    time_24_hours_ago = datetime.datetime.now() - datetime.timedelta(days=1)
    followings_list = [obj.followed_user for obj in request.user.profile.followings()]
    followings_signals = OrderOpenPosition.objects.filter(user__in=followings_list,result='S',created_datetime__gte=time_24_hours_ago)
    all_signals = OrderOpenPosition.objects.filter(result='S',created_datetime__gte=time_24_hours_ago,user__profile__is_signal_public=True)
    followings_posts = Post.objects.filter(user__in=followings_list)
    all_posts = Post.objects.filter(user__profile__is_post_public=True)
    if request.method == 'POST':
        post_form = PostForm(request.POST)
        if post_form.is_valid():
            post_obj = Post()
            post_obj.user = request.user
            post_obj.text_content = post_form.cleaned_data['text_content']
            post_obj.save()
            messages.success(request, ('Your post was successfully published!'))
            return redirect('feed_page')
        else:
            messages.error(request, ('Please correct the error below.'))
    else:
        post_form = PostForm()

    return render(request, 'social_media/feed_page.html', {
        'post_form': post_form,
        'followings_signals': followings_signals,
        'all_signals': all_signals,
        'followings_posts': followings_posts,
        'all_posts': all_posts,
        'user': request.user,
    })
