from django.urls import path
from .views import update_profile_page, like_logic, unlike_logic ,user_profile_page, follow_logic, unfollow_logic,feed_page


urlpatterns = [
    path('update-profile/', update_profile_page, name='update_profile_page'),
    path('like/<slug:post_id>/', like_logic, name='like_logic'),
    path('unlike/<slug:post_id>/', unlike_logic, name='unlike_logic'),
    path('<str:followed_user_username>/follow/', follow_logic, name='follow_logic'),
    path('<str:followed_user_username>/unfollow/', unfollow_logic, name='unfollow_logic'),
    path('<str:username>/', user_profile_page, name='user_profile_page'),
    path('feed', feed_page, name='feed_page'),

]
