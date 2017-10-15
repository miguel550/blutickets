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
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.views.generic import TemplateView
from tickets.views import TicketList, TicketDetailView
from sales.views import (create_order, edit_order_and_next,
                         checkout, remove_item_from_order,
                         slack_actions)
from contact.views import ContactFormView
from blutickets.TextView import load_text_view

urlpatterns = [
    # admin 
    url(r'^jet/', include('jet.urls', 'jet')),
    url(r'^jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),
    url(r'^select2/', include('django_select2.urls')),
    url(r'^admin/', admin.site.urls),

    # home
    url(r'^$', TicketList.as_view(), name='home'),
    # profiles
    url(r'^accounts/', include('allauth.urls')),
    # tickets
    url(r'^tickets/(?P<pk>[-\w]+)/$', TicketDetailView.as_view(), name='ticket-detail'),

    #text pages
    url(r'^(about|tos|privacy)/$', load_text_view, name='text'),

    # Sales
    url(r'^bucket/$', create_order, name='create_order_or_add_item'),
    url(r'^order/delete-item/$', remove_item_from_order, name='remove_item_from_order'),
    url(r'^edit-add-addresses/$', edit_order_and_next, name='edit_order_and_next'),
    url(r'^checkout/$', checkout, name='checkout'),
    # Contact
    url(r'^contact/$', ContactFormView.as_view(), name='contact'),
    # Slack app
    url(r'^slack/actions/$', slack_actions, name='slack_actions'),
]
handler404 = TicketList.as_view()

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    try:
        import debug_toolbar

        urlpatterns = [
                          url(r'^__debug__/', include(debug_toolbar.urls)),
                      ] + urlpatterns
    except ImportError:
        pass