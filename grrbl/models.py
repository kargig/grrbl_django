from django.db import models
from django import forms
from django.db.models.signals import post_save
from django.contrib.auth.models import User,Group
import datetime

# Create your models here.

B_OR_W = (
        ('b', 'Blacklist'),
        ('w', 'Whitelist'),
)

class IP(models.Model):
    ipaddress   = models.IPAddressField()
    dateadded   = models.DateTimeField('date added')
    reportedby  = models.ForeignKey(User)
    updated     = models.DateTimeField('last update',auto_now_add=True)
    attacknotes = models.TextField()
    b_or_w      = models.CharField(max_length=1, choices=B_OR_W)
    votes       = models.IntegerField(default=0)
    def __unicode__(self):
        return self.ipaddress

from django.forms import ModelForm
class IPform(ModelForm):
    class Meta:
        model = IP

class Vote(models.Model):
    user       = models.ForeignKey(User)
    ipaddress  = models.ForeignKey(IP)
    date       = models.DateTimeField('date added',auto_now_add=True)
    vote       = models.IntegerField(default=0)

class UserProfile(models.Model):
    user = models.OneToOneField(User)

    # Extra fields
    koko = models.BooleanField(default=False, blank=True)
    lala = models.CharField(max_length=20, default="foobar", blank=True)
    
    def __unicode__(self):
        return self.user.username

class GroupProfile(models.Model):
    group = models.OneToOneField(Group,null=True,blank=True)

    # Extra fields
    foobar = models.BooleanField()
    maxvotes = models.IntegerField(default=3)
    
    def __unicode__(self):
        return self.group.name


#ver1 -- works only with default values
def create_group_profile0(sender, **kw):
    mygroup = kw["instance"]
    if kw["created"]:
        profile = GroupProfile.objects.get_or_create(group=mygroup)

#ver2 -- works only with default values
def create_group_profile1(sender, **kw):
    mygroup = kw["instance"]
    if kw["created"]:
        profile = GroupProfile(group=mygroup)
        profile.save()

#ver3 -- works only with default values
def create_group_profile2(sender, instance, created, **kwargs):
    """Create a matching profile whenever a user object is created."""
    if created: 
        profile, new = GroupProfile.objects.get_or_create(group=instance)

#ver4 -- works only with default values
def create_group_profile3(sender, instance, created, **kwargs):
    """Create the GroupProfile when a new Group is saved"""
    if created:
        profile, new = GroupProfile.objects.get_or_create(group=instance)
        if new:
            profile.save()

#ver5 -- works only with default values
def create_group_profile4(sender, instance, created, **kwargs):
    if created:
        GroupProfile.objects.get_or_create(group=instance)

post_save.connect(create_group_profile3, sender=Group, dispatch_uid="group-profile-create-signal")
