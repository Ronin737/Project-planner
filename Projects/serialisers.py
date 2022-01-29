from rest_framework.serializers import ModelSerializer
from .models import Task,ProjectBoard
from Users.serialisers import Team
from django.shortcuts import get_object_or_404

'''Serializer classes for serializing the model data'''

class ProjectboardSerializer(ModelSerializer):

    class Meta:
        model=ProjectBoard
        exclude=['status','team']

    def get_fields(self, *args, **kwargs):
        fields = super().get_fields(*args, **kwargs)
        request = self.context.get('request').method
        if request is not None and not request=='POST':
            [fields.pop(key) for key in ['description','creation_time','assigned_team_id']]
        
        return fields

    def create(self, validated_data):
        teamid=validated_data.get('assigned_team_id')
        board=ProjectBoard.objects.create(**validated_data)
        team=get_object_or_404(Team.objects.all(),pk=teamid)
        board.team=team
        return board

class ProjectboardStatusSerializer(ModelSerializer):
    class Meta:
        model=ProjectBoard
        fields=['status']


class TaskSerializer(ModelSerializer):

    class Meta:
        model=Task
        exclude=['status','board','user']
    
    def create(self, validated_data):
        team=get_object_or_404(Team.objects.all(),pk=validated_data['team_id'])
        taskboard=team.board
        if(taskboard and taskboard.status=='OPEN'):
            if taskboard.task.all().filter(title=validated_data['title']):
                raise Exception("Task name must be unique")
        else:
            raise Exception('Project board is not available')
        task=Task.objects.create(**validated_data)
        task.user=team
        task.board=taskboard
        return task
    

class TaskStatusSerializer(ModelSerializer):

    class Meta:
        model=Task
        fields=['status']
