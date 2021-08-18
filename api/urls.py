from django.urls import path


from api.views import markets_page



urlpatterns = [
    path('markets', markets_page, name='markets_page'),

]
