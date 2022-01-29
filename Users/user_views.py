from .user_base import UserBase
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateAPIView
from .serialisers import TeamSerializer,User,UserSerializer

'''Available views for API endpoints'''

class CreateListUserAPI(ListCreateAPIView,UserBase):
    queryset=User.objects.all()
    serializer_class=UserSerializer

    def create_user(self, request):
        '''Overriding function for creating'''
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'id':serializer.data['user_id']}, status=status.HTTP_201_CREATED)
    
    def post(self,  request, *args, **kwargs):
        return self.create_user(request)

    def list_users(self):
        '''Overriding funciton for listing'''
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    def get(self,  request, *args, **kwargs):
        return self.list_users()


class DescribeUpdateTeamUserAPI(RetrieveUpdateAPIView,UserBase):
    queryset=User.objects.all()
    
    def get_serializer_class(self):
        '''Overriding function for getting the appropriate serializer'''
        if 'team' in self.kwargs:
            return TeamSerializer
        
        return UserSerializer

    def describe_user(self):
        '''Overriding function for getting detailed view'''
        item = self.get_object()
        serializer = self.get_serializer(item)
        return Response(serializer.data)
    
    def get(self,  request, *args, **kwargs):
        if(self.get_serializer_class()==TeamSerializer):
            return self.get_user_teams()
        return self.describe_user()
    
    
    def update_user(self, request,**kwargs):
        '''Overriding function for updating'''
        partial = kwargs.pop('partial', False)
        item = self.get_object()
        serializer = self.get_serializer(item, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_200_OK)
    
    def put(self,  request, *args, **kwargs):
        return self.update_user(request,**kwargs)
    
    def patch(self,  request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update_user(request,**kwargs)
    
    def get_user_teams(self):
        item = self.get_object()
        serializer = self.get_serializer(item.team)
        return Response(serializer.data)
    



    

    
    




