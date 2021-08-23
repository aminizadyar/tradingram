from django.urls import path
from .views import update_profile , like_logic


urlpatterns = [
    path('update-profile', update_profile, name='update_profile'),
    path('likes/<slug:post_id>/', like_logic, name='like_logic'),
]
