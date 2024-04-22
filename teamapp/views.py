from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Team
from userapp.models import User
from .serializers import * 

# Create your views here.
class CreateTeamAPIView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            data = request.data
            team_name = data.get('team_name')
            description = data.get('description')
            admin_id = data.get('user_id')

            if not team_name or not description or not admin_id:
                return Response({"error": "Missing fields"}, status=status.HTTP_400_BAD_REQUEST)

            if len(team_name) > 64 or len(description) > 128:
                return Response({"error": "Input length exceeds limit"}, status=status.HTTP_400_BAD_REQUEST)

            # Check for unique team name
            try:
                team_obj = Team.objects.get(name=team_name)
                return Response({"error": "Team name must be unique"}, status=status.HTTP_400_BAD_REQUEST)
            except:
                get_user = User.objects.get(id=admin_id)
                team_obj = Team(
                    team_name = team_name,
                    team_description =  description,
                    user= get_user
                )
                get_user.save()


            # Create team and generate a unique team_id
             

            return Response({"id": team_obj}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        

class ListTeamView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            users = Team.objects.all().values('team_name', 'team_description', 'created_timestamp','user')
            return Response(list(users))
        except User.DoesNotExist:
            return Response({"error": "User not found"})
        
            
class DescribeTeamView(APIView):
    def post(self, request, *args, **kwargs):
        team_id = request.data.get('team_id')
        try:
            team_obj = Team.objects.get(id=team_id)
            
            response = {
                "team_name": team_obj.team_name,
                "description": team_obj.team_description,
                "creation_time": team_obj.created_timestamp.isoformat(),
                "user":team_obj.user.id
            }
            return Response(response)
        except Team.DoesNotExist:
            return Response({"error": "Team not found"}, status=status.HTTP_404_NOT_FOUND)
        

class UpdateTeamAPIView(APIView):
    def post(self, request):
        # Parse incoming JSON data
        data = request.data
        print(data.get)
        try:

            team_id = data['id']
            team_data = data['team']
            team_name = team_data['team_name']
            team_description = team_data['team_description']
            admin_id = team_data['user']

            # Validate the team name length
            if len(team_name) > 64:
                return Response({"error": "Team name can be a maximum of 64 characters."}, status=status.HTTP_400_BAD_REQUEST)

            # Validate the team description length
            if len(team_description) > 128:
                return Response({"error": "Team description can be a maximum of 128 characters."}, status=status.HTTP_400_BAD_REQUEST)

            # Check for team uniqueness
            if Team.objects.exclude(id=team_id).filter(team_name=team_name).exists():
                return Response({"error": "A team with this name already exists."}, status=status.HTTP_400_BAD_REQUEST)

            # Find the team to update
            try:
                team = Team.objects.get(id=team_id)
            except Team.DoesNotExist:
                return Response({"error": "Team not found."}, status=status.HTTP_404_NOT_FOUND)

            # Update the team
            print("heree")
            team.team_name = team_name
            team.team_description = team_description
            team.user_id = admin_id  # Assuming admin is referenced by an ID and exists in the User model
            team.save()
            team_data={
            'team_name': team.team_name,
            "team_description":team.team_description,
            'user':team.user_id
        }
            return Response({"message": "Team updated successfully.","team_data":team_data}, status=status.HTTP_200_OK)
        
        except KeyError as e:
            # Handle missing keys in the input JSON
            return Response({"error": f"Missing key in the input data: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            # General exception handling (e.g., database issues)
            return Response({"error": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class AddUsersToTeamView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = AddUsersToTeamSerializer(data=request.data)
        if serializer.is_valid():
            team = serializer.validated_data['team']
            users = serializer.validated_data['users']
            # Checking current total users in the team
            if team.users.count() + len(users) > 50:
                return Response({"error": "Adding these users would exceed the 50 user limit for this team."},
                                status=status.HTTP_400_BAD_REQUEST)
            team.users.add(*users)  # Add users to the team
            return Response({"message": "Users added successfully to the team."}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class RemoveUsersFromTeamView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = RemoveUsersFromTeamSerializer(data=request.data)
        if serializer.is_valid():
            team = serializer.validated_data['team']
            users = serializer.validated_data['users']
            # Removing users from the team
            team.users.remove(*users)
            return Response({"message": "Users removed successfully from the team."}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListTeamUsersView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = TeamIdSerializer(data=request.data)
        if serializer.is_valid():
            team = serializer.validated_data['team']
            users = team.users.all()  # Ensure 'users' is the correct related name if set, or default to model name
            output_serializer = UserSerializer(users, many=True)
            return Response(output_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
