from django.urls import path
from .user_views import CreateListUserAPI,DescribeUpdateTeamUserAPI
from .team_views import CreateListTeamAPI,DescribeUpdateModifyTeamAPI,AddModifyDeleteUsersAPI

'''Valid API endpoints'''

team_urls=[path('Teams/',CreateListTeamAPI.as_view(),name='teamapi-create-list'),
            path('Teams/<str:pk>/',DescribeUpdateModifyTeamAPI.as_view(),name='teamapi-describe'),
            path('Teams/update/<str:pk>/',DescribeUpdateModifyTeamAPI.as_view(),name='teamapi-update'),
            path('Teams/users/<str:pk>/addusers/',AddModifyDeleteUsersAPI.as_view(),name='teamapi-addusers'),
            path('Teams/users/<str:pk>/deleteusers/',AddModifyDeleteUsersAPI.as_view(),name='teamapi-deleteusers'),
            path('Teams/users/<str:pk>/',AddModifyDeleteUsersAPI.as_view(),name='teamapi-listusers')]

user_urls=[path('',CreateListUserAPI.as_view(),name='userapi-create-list'),
            path('<str:pk>/',DescribeUpdateTeamUserAPI.as_view(),name='userapi-describe'),
            path('update/<str:pk>/',DescribeUpdateTeamUserAPI.as_view(),name='userapi-update'),
            path('user-team/<str:pk>/',DescribeUpdateTeamUserAPI.as_view(),{'team':True},name="userapi-userteam")]

urlpattern=team_urls+user_urls