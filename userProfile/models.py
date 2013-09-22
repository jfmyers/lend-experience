# Summary: Models for user Profiles, user Points and uploading Documents(for now this is profile pics only).
from django.db import models
from django.contrib.auth.models import User
from tags.models import Tags
import re

class Document(models.Model):
    file = models.FileField(upload_to='documents/%Y/%m/%d')
    
class Profile(models.Model):
    gender = models.CharField(max_length=50,blank=True)
    type = models.CharField(max_length=100, blank=True)
    hash_id = models.CharField(max_length=200,blank=True)
    fname = models.CharField(max_length=30,blank=True)
    lname = models.CharField(max_length=30,blank=True)
    handle = models.CharField(max_length=30,blank=True)
    dateJoined = models.DateTimeField(blank=True)
    company = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=30, blank=True)
    city = models.CharField(max_length=30, blank=True)
    state = models.CharField(max_length=20, blank=True)
    title = models.CharField(max_length=150, blank=True)
    industry = models.CharField(max_length=150, blank=True)
    about = models.CharField(max_length=2000, blank=True)
    pic = models.CharField(max_length=400, blank=True, default="default.png")
    dateJoined = models.DateTimeField(blank=True,null=True)
    linkedin_token = models.CharField(max_length=400, blank=True)
    linkedin_created = models.DateTimeField(blank=True,null=True)
    pass
    
    def __unicode__(self):
         return self.handle
         
    def clean_handle(self, handle):
        handle = re.sub(r'\W',"",handle)
        handle = handle.replace("_",'')
        handle = handle.strip()
        
        return handle
    
class Points(models.Model):
    user = models.OneToOneField(Profile,parent_link=True)
    total = models.IntegerField(blank=True, default=0)
    post_pts = models.IntegerField(blank=True, default=0)
    comment_pts = models.IntegerField(blank=True, default=0)
    vote_pts = models.IntegerField(blank=True, default=0)
    
    def __unicode__(self):
         return self.total