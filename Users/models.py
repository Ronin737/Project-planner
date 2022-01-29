from django.db import models
from django_extensions.db.models import AutoSlugField

class Team(models.Model):
    name=models.CharField(max_length=64,unique=True)
    description=models.TextField(max_length=128,blank=True)
    admin=models.CharField(max_length=50)
    creation_time=models.DateTimeField(auto_now_add=True)
    team_id=AutoSlugField(populate_from=['name','creation_time'], unique=True,primary_key=True,default='')


class User(models.Model):
    name=models.CharField(max_length=64)
    display_name=models.CharField(max_length=64,unique=True)
    creation_time=models.DateTimeField(auto_now_add=True)
    user_id=AutoSlugField(populate_from=['display_name','creation_time'], unique=True,primary_key=True,default='')
    team=models.ForeignKey(Team,on_delete=models.SET_NULL,null=True,blank=True,related_name='user')



