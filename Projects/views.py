from .serialisers import Task,TaskSerializer,ProjectBoard,ProjectboardSerializer,ProjectboardStatusSerializer,TaskStatusSerializer
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateAPIView
from .project_board_base import ProjectBoardBase
from rest_framework.response import Response
from rest_framework import status
import csv
from django.http import HttpResponse

'''Available views for API endpoints'''

class CreateBoardListAPI(ListCreateAPIView,ProjectBoardBase):
    queryset=ProjectBoard.objects.all()

    def get_queryset(self):
        '''Overriding function for getting appropriate queryset'''
        queryset=ProjectBoard.objects.all()
        if 'addtask' in self.kwargs:
            queryset=Task.objects.all()
        
        return queryset
        
    def get_serializer_class(self):
        '''Overriding function for getting appropriate serializer'''
        serializer_class=ProjectboardSerializer
        if 'addtask' in self.kwargs:
            serializer_class=TaskSerializer
        
        return serializer_class

    def create_board(self, request):
        '''Overriding function for creating'''
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'id':serializer.data['board_id']})
    
    def add_task(self, request):
        '''Extending function for adding'''
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'id':serializer.data['task_id']})

    
    def list_boards(self):
        '''Overriding function for listing'''
        queryset = self.get_queryset()
        openboards=queryset.filter(status='OPEN')
        serializer = self.get_serializer(openboards, many=True)
        return Response(serializer.data)
    
    def post(self,  request, *args, **kwargs):
        if 'addtask' in self.kwargs:
            return self.add_task(request)
        return self.create_board(request)
    
    def get(self,  request, *args, **kwargs):
        if('openboards' in self.kwargs):
            return self.list_boards()
        return self.list(request, *args, **kwargs)


class UpdateBoardTaskAPI(RetrieveUpdateAPIView,ProjectBoardBase):

    def get_queryset(self):
        '''Overriding function for getting appropriate queryset'''
        queryset=ProjectBoard.objects.all()
        if 'updatetask' in self.kwargs:
            queryset=Task.objects.all()
        return queryset

    def get_serializer_class(self):
        '''Overriding function for getting appropriate serializer'''
        serializer_class=ProjectboardStatusSerializer
        if 'updatetask' in self.kwargs:
            serializer_class=TaskStatusSerializer
        return serializer_class
    
    def close_board(self):
        '''Extending function for closing'''
        board=self.get_object()
        if board.task.filter(status='OPEN' or 'IN_PROGRESS'):
            raise Exception('Board cannot be closed with tasks pending')
        serializer = self.get_serializer(board, data={'status':'CLOSED'})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)
    
    def update_task_status(self, request):
        '''Extendng function for updating'''
        task = self.get_object()
        serializer = self.get_serializer(task, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)
    
    def put(self, request, *args, **kwargs):
        if 'updatetask' in self.kwargs:
            return self.update_task_status(request)
        return self.close_board()

        
class ExportBoardAPI(RetrieveUpdateAPIView,ProjectBoardBase):
    queryset=ProjectBoard.objects.all()
    serializer_class=ProjectboardSerializer

    def export_board(self):
        '''Extending function for exporting'''
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="export.csv"'
        writer = csv.writer(response)
        board=self.get_object()
        serializer=self.get_serializer(board)
        serializer['status']=board.status
        tasks=board.task.all()
        serialised_tasks=TaskSerializer(tasks,many=True)
        rows=[f'{field}:{value}' for field,value in serializer.items()]
        writer.writerows(rows)
        writer.writerow('Tasks:-')
        trows=[[f'{field}:{value}' for field,value in task.items()] for task in serialised_tasks]
        writer.writerows(trows)

        return response
    
    def get(self, request, *args, **kwargs):
        return self.export_board()


        
        
        








    


        
        