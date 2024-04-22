from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User

class CreateUserView(APIView):
    def post(self, request, *args, **kwargs):
        
        try:
            unique_name = request.data['name']
            get_user_obj = User.objects.get(name=unique_name)
            error_msg = "User name is already present please try again."
            response = {"error": error_msg}
            return Response(response)
        except User.DoesNotExist:
            user = User.objects.create(name=request.data['name'], display_name=request.data['display_name'])
            response = {"id": user.id}
            return Response(response)

class ListUsersView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            users = User.objects.all().values('name', 'display_name', 'creation_time')
            return Response(list(users))
        except User.DoesNotExist:
            return Response({"error": "User not found"})

class DescribeUserView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            user_id = request.data.get('user_id')
            user = User.objects.get(id=user_id)
            response = {
                "name": user.name,
                "display_name": user.display_name,
                "creation_time": user.creation_time.isoformat()
            }
            return Response(response)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

class UpdateUserAPIView(APIView):
    def post(self, request, *args, **kwargs):
        # Parse the request JSON
        try:
            update_data = request.data
        except ValueError:
            return Response({"error": "Invalid JSON"}, status=status.HTTP_400_BAD_REQUEST)
        
        user_id = update_data.get('id')
        new_display_name = update_data.get('user', {}).get('display_name')
        
        # Validate input data
        if not user_id or not new_display_name:
            return Response({"error": "Invalid request"}, status=status.HTTP_400_BAD_REQUEST)

        # Check constraints
        if len(new_display_name) > 128:
            return Response({"error": "Display name must be within 128 characters"}, status=status.HTTP_400_BAD_REQUEST)
        
        user = User.objects.get(id=user_id)
        user.display_name = new_display_name
        user.save()
        user_data={
            'user_name': user.name,
            "display_name":user.display_name
        }

        return Response({"message": "User updated successfully","update_user_data":user_data}, status=status.HTTP_200_OK)

class GetUserTeamsAPIView(APIView):
    def post(self, request):
        # Parse incoming JSON data
        data = request.data
        try:
            user_id = data['id']
            user = User.objects.get(pk=user_id)
            teams = user.team_set.all()
            # Construct the list of team data
            team_list = [
                {
                    "name": team.team_name,
                    "description": team.team_description,
                    "creation_time": team.created_timestamp.strftime("%Y-%m-%d %H:%M:%S")
                }
                for team in teams
            ]

            return Response(team_list, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        except KeyError:
            return Response({"error": "Missing user ID in request."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




