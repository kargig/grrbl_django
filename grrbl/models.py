from django import forms
from django.db import models
from django.forms import ModelForm
from django.db.models.signals import post_save
from django.contrib.auth.models import User,Group
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
import datetime

# Create your models here.

B_OR_W = (
        ('b', 'Blacklist'),
        ('w', 'Whitelist'),
)

class VotableObject(models.Model):
    votes = models.IntegerField(default=0)

    class Meta:
        abstract = True


class IP(VotableObject):
    ipaddress   = models.IPAddressField()
    dateadded   = models.DateTimeField('date added')
    reportedby  = models.ForeignKey(User, related_name='ip_repby')
    updated     = models.DateTimeField('last update',auto_now_add=True)
    attacknotes = models.TextField()
    b_or_w      = models.CharField(max_length=1, choices=B_OR_W)
    def __unicode__(self):
        return self.ipaddress


class IPform(ModelForm):
    class Meta:
        model = IP


class Email(VotableObject):
    emailaddress = models.EmailField()
    dateadded    = models.DateTimeField('date added')
    reportedby   = models.ForeignKey(User, related_name='email_repby')
    updated      = models.DateTimeField('last update',auto_now_add=True)
    attacknotes  = models.TextField()
    b_or_w       = models.CharField(max_length=1, choices=B_OR_W)

    def __unicode__(self):
        return self.emailaddress


class Emailform(ModelForm):
    class Meta:
        model = Email


class Vote(models.Model):
    user       = models.ForeignKey(User)
    content_type  = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    item = generic.GenericForeignKey('content_type', 'object_id')
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
    weight = models.IntegerField(default=3)
    
    def __unicode__(self):
        return self.group.name

