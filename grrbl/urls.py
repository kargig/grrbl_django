from django.conf.urls.defaults import *
from django.contrib.auth.decorators import login_required
from django.views.generic.simple import direct_to_template
from django.contrib.auth.views import login, logout
from grrbl.models import *

ip_dict = {
    'queryset': IP.objects.all(),
}

email_dict = {
    'queryset': Email.objects.all(),
}

urlpatterns = patterns('',
    #(r'^list/$','django.views.generic.list_detail.object_list', { 
    (r'^$','grrbl.views.main_page'),
    (r'^iplist/$','grrbl.views.auth_list', {
        'queryset': IP.objects.all().order_by('-dateadded'),
        'template_name': 'grrbl/iplist.html',
    }, 'ip_list'),
    (r'^emaillist/$','grrbl.views.auth_list', {
        'queryset': Email.objects.all().order_by('-dateadded'),
        'template_name': 'grrbl/emaillist.html',
    }, 'email_list'),
    (r'^ipdetails/(?P<object_id>\d+)/$', 'django.views.generic.list_detail.object_detail',
        dict(ip_dict,template_name='grrbl/ipdetail.html'), 'ip_details'),
    (r'^ipdetails/(?P<ipaddress>((([0-2]?\d{0,2}\.){3}([0-2]?\d{0,2}))|(([\da-fA-F]{1,4}:){7}([\da-fA-F]{1,4}))))$', 'grrbl.views.my_ipdetail' ),
    (r'^emaildetails/(?P<emailaddress>[a-z0-9!#$%&\'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&\'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?)$', 'grrbl.views.my_emdetail' ),
    (r'^emaildetails/(?P<object_id>\d+)/$', 'django.views.generic.list_detail.object_detail',
        dict(email_dict,template_name='grrbl/emaildetail.html'), 'email_details'),
    (r'^details/(?P<object_type>\w+)/(?P<object_id>\d+)/vote/$', 'grrbl.views.vote'),
    (r'^login/$', 'django.contrib.auth.views.login'),
    (r'^logout/$', logout),
    (r'^accounts/', include('captcha.backends.default.urls')),
    (r'^accounts/', include('registration.backends.default.urls')),
)
