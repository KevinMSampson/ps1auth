from django.conf.urls import patterns, include, url
from django.core.urlresolvers import reverse
from django.views.generic import RedirectView
from django.views.decorators.csrf import csrf_exempt

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from money.models import *

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'auth.views.home', name='home'),
    url(r'^$', RedirectView.as_view(permanent=False, url='/zoho/member_list')),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^rfid/', include('rfid.urls')),
    url(r'^zoho/', include('zoho_integration.urls')),
    url(r'^admin/', include(admin.site.urls)),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
)
