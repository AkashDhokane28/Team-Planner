from rest_framework import serializers
from .models import Board,Task
from teamapp.models import Team

class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ['id', 'board_name', 'board_description', 'team', 'created_time']

    def validate_board_name(self, value):
        # This method receives just the value of `board_name`, not a dictionary
        if len(value) > 64:
            raise serializers.ValidationError("The board name must be at most 64 characters long.")
        
        # Uniqueness within a team is handled in the `validate` method
        return value

    def validate_board_description(self, value):
        # This method receives just the value of `board_description`, not a dictionary
        if len(value) > 128:
            raise serializers.ValidationError("The board description must be at most 128 characters long.")
        return value

    def validate(self, data):
        # Ensuring the board name is unique within the same team
        if 'team' in data and 'board_name' in data:
            if Board.objects.filter(team=data['team'], board_name=data['board_name']).exists():
                raise serializers.ValidationError({"board_name": "A board with this name already exists within the team."})
        return data
    
class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'user_id', 'board', 'creation_time']

    def validate_title(self, value):
        # Additional unique validation can be implemented in the view if needed
        if len(value) > 64:
            raise serializers.ValidationError("The title must be at most 64 characters long.")
        return value

    def validate_description(self, value):
        if len(value) > 128:
            raise serializers.ValidationError("The description must be at most 128 characters long.")
        return value