from rest_framework import serializers
from userapp.models import User
from .models import Team

class AddUsersToTeamSerializer(serializers.Serializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Team.objects.all(), source='team')
    users = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True)

    def validate_users(self, value):
        if len(value) > 50:
            raise serializers.ValidationError("Cannot add more than 50 users at a time.")
        return value

class RemoveUsersFromTeamSerializer(serializers.Serializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Team.objects.all(), source='team')
    users = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True)


class TeamIdSerializer(serializers.Serializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Team.objects.all(), source='team')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'display_name')

    