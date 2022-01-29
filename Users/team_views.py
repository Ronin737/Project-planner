from .serialisers import TeamSerializer,UserIDSerializer,Team,User
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateAPIView,RetrieveUpdateDestroyAPIView
from .team_base import TeamBase
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

'''Available views for API endpoints'''

class CreateListTeamAPI(ListCreateAPIView,TeamBase):
    serializer_class=TeamSerializer
    queryset=Team.objects.all()

    def create_team(self, request):
        '''Overriding function for creating'''
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'id':serializer.data['team_id']})
    
    def post(self,  request, *args, **kwargs):
        return self.create_team(request)

    def list_teams(self):
        '''Overriding function for lisitng'''
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    def get(self,  request, *args, **kwargs):
        return self.list_teams()


class DescribeUpdateModifyTeamAPI(RetrieveUpdateAPIView,TeamBase):
    queryset=Team.objects.all()
    serializer_class=TeamSerializer

    def describe_team(self):
        '''Overriding function for detailed view'''
        item = self.get_object()
        serializer = self.get_serializer(item)
        return Response(serializer.data)
    
    def get(self,  request, *args, **kwargs):
        return self.describe_team()
    
    def update_team(self, request,**kwargs):
        '''Overriding function for updating'''
        partial = kwargs.pop('partial', False)
        item = self.get_object()
        serializer = self.get_serializer(item, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_200_OK)
    
    def put(self,  request, *args, **kwargs):
        return self.update_team(request,**kwargs)
    
    def patch(self,  request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update_team(request,**kwargs)


class AddModifyDeleteUsersAPI(RetrieveUpdateDestroyAPIView,TeamBase):
    queryset=Team.objects.all()
    serializer_class=UserIDSerializer
    
    def add_users_to_team(self, request):
        '''Extending function for adding'''
        userslist=request.PUT.get('users') or request.PATCH.get('users')
        item=self.get_object()
        overflow=False
        for user in userslist:
            if item.user_set.count()== 50:
                overflow=True
                break
            userinstance=get_object_or_404(User.objects.all,pk=user)
            userinstance.team.add(item)
        
        if(overflow):
            raise Exception("No vacancy")
        
        return Response(status=status.HTTP_200_OK)
    
    def remove_users_from_team(self, request):
        '''Extending function for removing'''
        userslist=request.DELETE.get('users')
        item=self.get_object()
        for user in userslist:
            userinstance=get_object_or_404(User.objects.all,pk=user)
            item.user_set.remove(user)
        
        return Response(status=status.HTTP_200_OK)
    
    def list_team_users(self, request):
        '''Extending function for listing'''
        item=self.get_object()
        queryset = User.objects.filter(team=item)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)
    
    def get(self, request, *args, **kwargs):
        return self.list_team_users(request)
    
    def put(self, request, *args, **kwargs):
        return self.add_users_to_team(request)
    
    def patch(self, request, *args, **kwargs):
        return self.add_users_to_team(request)
    
    def delete(self, request, *args, **kwargs):
        return self.remove_users_to_team(request)
    
    
        
        

        


        
