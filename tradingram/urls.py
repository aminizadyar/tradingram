"""tradingram URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from paper_trade.urls import urlpatterns as paper_trade_urlpatterns
from landing_page.urls import urlpatterns as landing_page_urlpatterns
from api.urls import urlpatterns as api_urlpatterns
from social_media.urls import urlpatterns as social_media_urlpatterns

from django.conf import settings
from django.conf.urls.static import static





urlpatterns = [
    path('admin/', admin.site.urls),
] + paper_trade_urlpatterns + landing_page_urlpatterns + api_urlpatterns + social_media_urlpatterns

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)