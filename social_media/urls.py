from django.urls import path
from .views import update_profile_page , like_logic , user_profile_page


urlpatterns = [
    path('update-profile/', update_profile_page, name='update_profile_page'),
    path('likes/<slug:post_id>/', like_logic, name='like_logic'),
    path('<str:username>/', user_profile_page, name='user_profile_page'),
]
