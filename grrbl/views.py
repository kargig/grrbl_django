# Create your views here.
#from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
#from django.template import Context, loader, RequestContext
from django.views.decorators.csrf import csrf_protect
from django.views.generic.list_detail import object_detail 
from django.views.generic.list_detail import object_list 
from django.contrib.auth.decorators import login_required
from grrbl.models import *
from django.core.urlresolvers import reverse

from django.http import HttpResponseRedirect

def logout_page(request):
    """
    Log users out and re-direct them to the main page.
    """
    logout(request)
    return HttpResponseRedirect('/grrbl/logout.html')

#@login_required
def main_page(request):
    """
    If users are authenticated, direct them to the main page. Otherwise, take
    them to the login page.
    """
    return render_to_response('grrbl/index.html')

@login_required 
def auth_list(*args, **kwargs):
        return object_list(*args, **kwargs) 

@login_required
def vote(request, ip_id):
    p = get_object_or_404(IPS, pk=ip_id)
    try:
        selected_ip = p #change to if user has voted this IP before
    except (KeyError, IPS.DoesNotExist):
        # Redisplay the poll voting form.
        return render_to_response('grrbl/detail.html', {
            'ips': p,
            'error_message': "You didn't select a choice.",
        }, context_instance=RequestContext(request))
    else:
        selected_ip.votes += int(request.POST['vote'])
        selected_ip.save()
        return HttpResponseRedirect(reverse('ip_details', args=(p.id,)))
