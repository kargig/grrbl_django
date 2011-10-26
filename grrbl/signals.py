from django.db.models.signals import post_save
from django.contrib.auth.models import Group
from models import GroupProfile
from django.db import models

#ver1 -- works only with default values
def create_group_profile(sender, **kw):
    mygroup = kw["instance"]
    print "DEBUG"
    if kw["created"]:
        profile = GroupProfile.objects.get_or_create(group=mygroup)


#ver2 -- works only with default values
def create_group_profile1(sender, **kw):
    mygroup = kw["instance"]
    if kw["created"]:
        profile = GroupProfile()
        profile.group = mygroup
        profile.save()

def create_group_profile2(sender, instance, created, **kwargs):
    """Create a matching profile whenever a user object is created."""
    if created: 
        profile, new = GroupProfile.objects.get_or_create(group=instance)


post_save.connect(create_group_profile2, sender=Group, dispatch_uid="groups-profilecreation-signal")
