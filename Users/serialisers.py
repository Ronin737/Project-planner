from rest_framework.serializers import ModelSerializer
from .models import Team,User

'''Serializer classes for serializing the model data'''

class TeamSerializer(ModelSerializer):

    class Meta:
        model=Team
        fields='__all__'

    def get_fields(self, *args, **kwargs):
        fields = super().get_fields(*args, **kwargs)
        request = self.context.get('request').method
        if request is not None and not request=='POST':
            fields.pop('team_id')
        return fields

class UserSerializer(ModelSerializer):
    class Meta:
        model=User
        exclude=['team']
    
    def get_fields(self, *args, **kwargs):
        fields = super().get_fields(*args, **kwargs)
        request = self.context.get('request').method
        if request is not None and not request=='POST':
            fields.pop('user_id')
        return fields

class UserIDSerializer(ModelSerializer):

    class Meta:
        model=User
        exclude=['team','creation_time']
        


