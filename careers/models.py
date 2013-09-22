# Summary: Every career area (Business, Education, Energy...) is associated with Career Subareas.
from django.db import models

class SubArea(models.Model):
    name = models.CharField(max_length=75)

class Area(models.Model):
    name = models.CharField(max_length=75)
    url = models.CharField(max_length=75)
    pic = models.CharField(max_length=30)
    subarea = models.ManyToManyField(SubArea)