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
    }),
    (r'^emaillist/$','grrbl.views.auth_list', {
        'queryset': Email.objects.all().order_by('-dateadded'),
        'template_name': 'grrbl/emaillist.html',
    }),
    (r'^ipdetails/(?P<object_id>\d+)/$', 'django.views.generic.list_detail.object_detail',
        dict(ip_dict,template_name='grrbl/ipdetail.html'), 'ip_details'),
    (r'^emaildetails/(?P<object_id>\d+)/$', 'django.views.generic.list_detail.object_detail',
        dict(email_dict,template_name='grrbl/emaildetail.html'), 'email_details'),
    (r'^details/(?P<object_type>\w+)/(?P<object_id>\d+)/vote/$', 'grrbl.views.vote'),
    (r'^login/$', 'django.contrib.auth.views.login'),
    (r'^logout/$', logout)
)
