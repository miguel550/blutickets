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
from graphene_django.views import GraphQLView

from tickets.views import TicketList, TicketDetailView, OnlyTicketList
from sales.views import (create_order, edit_order_and_next,
                         checkout, remove_item_from_order,
                         slack_actions)
from profiles.views import SignupLogin, SignUp, Login
from contact.views import ContactFormView
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    # admin
    url(r'^jet/', include('jet.urls', 'jet')),
    url(r'^jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),
    url(r'^select2/', include('django_select2.urls')),
    url(r'^panel/admin/', admin.site.urls),

    # home
    url(r'^$', TicketList.as_view(template_name='pages/home.html'), name='home'),
    # profiles
    url(r'^accounts/login', Login.as_view(), name="login"),
    url(r'^accounts/signup', SignUp.as_view(), name="signup"),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^enter/$', SignupLogin.as_view(), name="login-signup"),
    # tickets
    url(r'^tickets/(?P<slug>[a-zA-Z0-9-]+)/$', TicketDetailView.as_view(), name='ticket-detail'),
    url(r'^tickets/$', OnlyTicketList.as_view(), name='tickets'),

    # text pages
    url(r'^about/$', TemplateView.as_view(template_name='text/about.html'), name='who-we-are'),
    url(r'^tos/$', TemplateView.as_view(template_name='text/tos.html'), name='tos'),
    url(r'^privacy/$', TemplateView.as_view(template_name='text/privacy.html'), name='privacy'),

    # Sales
    url(r'^bucket/$', create_order, name='create_order_or_add_item'),
    url(r'^order/delete-item/$', remove_item_from_order, name='remove_item_from_order'),
    url(r'^edit-add-addresses/$', edit_order_and_next, name='edit_order_and_next'),
    url(r'^checkout/$', checkout, name='checkout'),
    # Contact
    url(r'^contact/$', ContactFormView.as_view(), name='contact'),
    # Slack app
    url(r'^slack/actions/$', slack_actions, name='slack_actions'),
    url(r'^graphql$', csrf_exempt(GraphQLView.as_view(graphiql=True))),
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
