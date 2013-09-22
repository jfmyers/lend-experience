from django.db import models
import re

class Tags(models.Model):
    name = models.CharField(max_length=70, blank=True)
    handle = models.CharField(max_length=70, blank=True)
    
    # Every tag has a handle used when viewing a tag page. The handle needs to be Url Safe.
    def clean_handle(self, handle):
        handle = re.sub(r'\W',"",handle)
        handle = handle.replace("_",'')
        handle = handle.strip()
        
        return handle