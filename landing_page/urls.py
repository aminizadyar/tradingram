from django.urls import path

from landing_page.views import landing_page

urlpatterns = [
    path('index', landing_page, name='landing_page'),
]
