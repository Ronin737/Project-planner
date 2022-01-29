from email.policy import default
from django.db import models
from django_extensions.db.models import AutoSlugField
from Users.models import Team

class ProjectBoard(models.Model):
    name=models.CharField(max_length=64,unique=True)
    description=models.TextField(max_length=128,blank=True)
    creation_time=models.DateTimeField()
    board_id=AutoSlugField(populate_from=['name','creation_time'],primary_key=True,default='')
    assigned_team_id=models.CharField('Team ID',max_length=50,blank=True)
    status=models.CharField(max_length=6,choices=[('OPEN','OPEN'),('CLOSED','CLOSED')],default='OPEN')
    team=models.OneToOneField(Team,on_delete=models.SET_NULL,null=True,default=None,related_name='board')
    

class Task(models.Model):
    title=models.CharField(max_length=64)
    description=models.TextField(max_length=128,blank=True)
    creation_time=models.DateTimeField()
    team_id=models.CharField('User ID',max_length=50,blank=True)
    task_id=AutoSlugField(populate_from=['title','creation_time'],primary_key=True,default='')
    status=models.CharField(max_length=12,choices=[('OPEN','OPEN'),('IN PROGRESS','IN_PROGRESS'),('COMPLETE','COMPLETE')],default='OPEN')
    board=models.ForeignKey(ProjectBoard,on_delete=models.CASCADE,related_name='task',default='')
    user=models.OneToOneField(Team,on_delete=models.SET_NULL,null=True,default=None)








