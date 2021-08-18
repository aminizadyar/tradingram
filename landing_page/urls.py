from django.urls import path
from landing_page.views import landing_page
from landing_page.views import signup_page


urlpatterns = [
    path('', landing_page, name='landing_page'),
    path('signup', signup_page, name='signup_page'),
]
