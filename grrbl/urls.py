from django.conf.urls.defaults import *
from django.contrib.auth.decorators import login_required
from django.views.generic.simple import direct_to_template
from django.contrib.auth.views import login, logout
from grrbl.models import *

info_dict = {
    'queryset': IP.objects.all(),
}
urlpatterns = patterns('',
    #(r'^list/$','django.views.generic.list_detail.object_list', { 
    (r'^$','grrbl.views.main_page'),
    (r'^list/$','grrbl.views.auth_list', {
        'queryset': IP.objects.all().order_by('-dateadded'),
        'template_name': 'grrbl/list.html',
    }),
    (r'^details/(?P<object_id>\d+)/$', 'django.views.generic.list_detail.object_detail',
        dict(info_dict,template_name='grrbl/detail.html'), 'ip_details'),
    (r'^details/(?P<ip_id>\d+)/vote/$', 'grrbl.views.vote'),
    (r'^login/$', 'django.contrib.auth.views.login'),
    (r'^logout/$', logout)
)
