"""blutickets URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.views.generic import TemplateView
from tickets.views import TicketList


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', TicketList.as_view(), name='home'),
    url(r'^who-we-are/$', TemplateView.as_view(template_name='who-we-are.html'), name='who-we-are'),
    url(r'^terms-and-conditions/$', TemplateView.as_view(template_name='terms-and-conditions.html'), name='terms'),
    url(r'^privacy/$', TemplateView.as_view(template_name='privacy.html'), name='privacy'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)