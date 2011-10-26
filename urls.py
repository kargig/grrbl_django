from django.conf.urls.defaults import *
from grrbl_django.views import *


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^$', main_page ),
    (r'^grrbl/', include('grrbl.urls')),
)
urlpatterns += patterns('',
    (r'^admin/', include(admin.site.urls))
)
