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
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect, HttpResponseForbidden, HttpResponseBadRequest

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
def vote(request, object_type, object_id):
    # Fetch the equivalend content types
    content_type = get_object_or_404(ContentType, app_label="grrbl", name=object_type)
    # Get the model classes
    object_class = content_type.model_class()

    objekt = get_object_or_404(object_class, pk=object_id)
    if not isinstance(objekt, VotableObject):
        return HttpResponseForbidden("Will not add vote to a"
                                     " non-votable object")

    try:
        vote_value = int(request.POST['vote'])
    except (ValueError, KeyError):
        # Malformed POST value
        return HttpResponseBadRequest("Bad vote value")

    try:
        vote = Vote.objects.get(content_type=content_type,
                                object_id=objekt.id,
                                user=request.user)
        # Subtract the previous vote value
        objekt.votes -= vote.vote
    except Vote.DoesNotExist:
        vote = Vote(user=request.user, item=objekt, vote=int(request.POST['vote']))

    vote.vote = vote_value
    objekt.votes += vote_value
    objekt.save()
    vote.save()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
