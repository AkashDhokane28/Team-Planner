from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from .models import Board,Task
from django.utils import timezone
from teamapp.models import Team
import os
from django.http import JsonResponse

class CreateBoardView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = BoardSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'id': serializer.data['id']}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CloseBoardView(APIView):
    def post(self, request, *args, **kwargs):
        board_id = request.data.get('id')
        if not board_id:
            return Response({'error': 'Board ID is required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            board = Board.objects.get(id=board_id)
            if board.status == 'CLOSED':
                return Response({'error': 'This board is already closed.'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Check if all tasks are complete
            task =Task.objects.filter(board=board)
            if task:
                for i in task:
                    if i.status == "COMPLETED":
                        board.status = 'CLOSED'
                        board.end_time = timezone.now()
                        board.save()

                        return Response({'message': 'Board closed successfully.'}, status=status.HTTP_200_OK)
                    else:
                        return Response({'error': 'All tasks must be marked as COMPLETE before closing the board.'},
                        status=status.HTTP_400_BAD_REQUEST)
        except Board.DoesNotExist:
            return Response({'error': 'Board not found.'}, status=status.HTTP_404_NOT_FOUND)
        
class AddTaskView(APIView):
    def post(self, request):
        data = request.data
        try:
            board = Board.objects.get(id=data['board'])
            if board.status != 'OPEN':
                return Response({'error': 'Tasks can only be added to an OPEN board.'}, status=status.HTTP_400_BAD_REQUEST)

            serializer = TaskSerializer(data=data)
            if serializer.is_valid():
                # Check for unique title constraint within the board
                if Task.objects.filter(title=data['title'], board=board).exists():
                    return Response({'error': 'A task with this title already exists on this board.'}, status=status.HTTP_400_BAD_REQUEST)
                print("getting here")
                serializer.save(board=board, user_id=board.team , status="OPEN")  # Assuming `user` is passed in and authenticated
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Board.DoesNotExist:
            return Response({'error': 'Board not found.'}, status=status.HTTP_404_NOT_FOUND)


class UpdateTaskStatusAPIView(APIView):
    def post(self, request):
        data = request.data
        try:
            task_id = data.get('id')
            new_status = data.get('status')
            task = Task.objects.get(id=task_id)
            if new_status not in [choice[0] for choice in Task.STATUS_CHOICES]:
                return Response({'error': 'Invalid status provided'}, status=status.HTTP_400_BAD_REQUEST)

            task.status = new_status
            task.save()

            return Response({'message': 'Task status updated successfully'}, status=status.HTTP_200_OK)

        except Task.DoesNotExist:
            return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class ListBoardsAPIView(APIView):
    def post(self, request, *args, **kwargs):
        team_id = request.data.get('id')
        if not team_id:
            return Response({'error': 'Team ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            team = Board.objects.filter(team_id=team_id)
            
            boards_data = [{'id': board.id, 'name': board.board_name} for board in team]
            return Response(boards_data, status=status.HTTP_200_OK)

        except Team.DoesNotExist:
            return Response({'error': 'Team not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class ExportBoardAPIView(APIView):
    def post(self, request, *args, **kwargs):
        board_id = request.data.get('id')
        if not board_id:
            return JsonResponse({'error': 'Board ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            board = Board.objects.get(id=board_id)
        except Board.DoesNotExist:
            return JsonResponse({'error': 'Board not found'}, status=status.HTTP_404_NOT_FOUND)

        tasks = Task.objects.filter(board=board).order_by('creation_time')
        print('tasks',tasks)

        out_file_name = f'board_{board_id}.txt'
        out_path = os.path.join('out', out_file_name)

        os.makedirs('out', exist_ok=True)

        with open(out_path, 'w') as file:
            file.write(f"Board Name: {board.board_name}\n")
            file.write(f"Board Description: {board.board_description}\n")
            file.write(f"Board Status: {board.status}\n\n")
            file.write("Tasks:\n")
            for task in tasks:
                file.write(f"- Title: {task.title}\n")
                file.write(f"  Description: {task.description}\n")
                file.write(f"  Status: {task.status}\n")
                
        return JsonResponse({'out_file': out_file_name}, status=status.HTTP_200_OK)