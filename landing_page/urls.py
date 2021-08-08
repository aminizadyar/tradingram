from django.urls import path
from landing_page.views import landing_page
from landing_page.views import registration_completed

urlpatterns = [
    path('', landing_page, name='landing_page'),
    path('registration-completed', registration_completed, name='registration_completed'),
]
