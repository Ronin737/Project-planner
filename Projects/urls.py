from django.urls import path
from .views import CreateBoardListAPI,UpdateBoardTaskAPI,ExportBoardAPI

'''Valid API endpoints'''

urlpatterns=[path('Home/',CreateBoardListAPI.as_view(),name='boardapi-list-create'),
            path('Home/open-boards/',CreateBoardListAPI.as_view(),{'openboards':True},name='boardapi-list-openboards'),
            path('Home/add-task/',CreateBoardListAPI.as_view(),{'addtask':True},name='boardapi-addtasks'),
            path('Home/close-board/<str:pk>/',UpdateBoardTaskAPI.as_view(),name='boardapi-closeboard'),
            path('Home/update-task/<str:pk>/',UpdateBoardTaskAPI.as_view(),{'updatetask':True},name='boardapi-updatetask'),
            path('Home/export-board/<str:pk>',ExportBoardAPI.as_view(),name='boardapi-export')]