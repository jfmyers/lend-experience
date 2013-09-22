# Summary: Models for contributions(aka Posts) and contributions' comments(aka Comments).
import re
from django.db import models
from django.contrib.auth.models import User
from userProfile.models import Profile
from tags.models import Tags

class Comments(models.Model):
    contribution_id = models.IntegerField()
    user = models.OneToOneField(Profile,parent_link=True)
    text = models.CharField(max_length=1500,blank=True)
    date_created = models.IntegerField(max_length=20)
    remove = models.IntegerField(max_length=1,default=0)
    pass
    
    def __unicode__(self):
         return self.profile.fname
    
    class Meta:
        ordering = ('-date_created',)
    
class Posts(models.Model):
    type = models.CharField(max_length=20,blank=True)
    uid_old = models.CharField(max_length=150,blank=True)
    user = models.OneToOneField(Profile,parent_link=True)
    title = models.CharField(max_length=300)
    url = models.CharField(max_length=300,blank=True)
    description = models.CharField(max_length=12000)
    formatted_description = models.CharField(max_length=20000,blank=True)
    date_created = models.IntegerField(max_length=20,blank=True)
    remove = models.IntegerField(max_length=1,default=0)
    comments = models.ManyToManyField(Comments)
    tags = models.ManyToManyField(Tags)
    rating = models.IntegerField(blank=True)
    ArtDesignFashion = models.IntegerField(max_length=1, default=0, blank=True)
    Business = models.IntegerField(max_length=1, default=0, blank=True)
    Education = models.IntegerField(max_length=1, default=0, blank=True)
    Energy = models.IntegerField(max_length=1, default=0, blank=True)
    Engineering = models.IntegerField(max_length=1, default=0, blank=True)
    Entertainment = models.IntegerField(max_length=1, default=0, blank=True)
    GovernmentAndLaw = models.IntegerField(max_length=1, default=0, blank=True)
    HealthAndMedicine = models.IntegerField(max_length=1, default=0, blank=True)
    NonProfits = models.IntegerField(max_length=1, default=0, blank=True)
    Technology = models.IntegerField(max_length=1, default=0, blank=True)
    
    def __unicode__(self):
         return self.title
        
    # Every post has a handle/url used when viewing a post's page. The url needs to be Url Safe.
    def clean_title(self, title):
        url = re.sub(r'\W',"",title)
        url = url.replace("_",'')
        url = url.strip()
        
        return url