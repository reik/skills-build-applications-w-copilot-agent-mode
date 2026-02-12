from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    UserProfile, ActivityType, Activity, Team, 
    Leaderboard, Achievement, Challenge
)

class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id']


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for UserProfile model"""
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = UserProfile
        fields = [
            'id', 'user', 'bio', 'profile_picture', 'fitness_level',
            'date_of_birth', 'total_points', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'total_points']


class ActivityTypeSerializer(serializers.ModelSerializer):
    """Serializer for ActivityType model"""
    class Meta:
        model = ActivityType
        fields = ['id', 'name', 'description', 'base_points_per_unit', 'unit']
        read_only_fields = ['id']


class ActivitySerializer(serializers.ModelSerializer):
    """Serializer for Activity model"""
    activity_type = ActivityTypeSerializer(read_only=True)
    activity_type_id = serializers.PrimaryKeyRelatedField(
        queryset=ActivityType.objects.all(),
        source='activity_type',
        write_only=True
    )
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Activity
        fields = [
            'id', 'user', 'activity_type', 'activity_type_id', 
            'distance_or_duration', 'calories_burned', 'points_earned',
            'description', 'logged_at', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']


class TeamSerializer(serializers.ModelSerializer):
    """Serializer for Team model"""
    created_by = UserSerializer(read_only=True)
    members = UserSerializer(many=True, read_only=True)
    members_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Team
        fields = [
            'id', 'name', 'description', 'created_by', 'members',
            'members_count', 'total_points', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_by', 'created_at', 'updated_at', 'total_points']
    
    def get_members_count(self, obj):
        return obj.members.count()


class LeaderboardSerializer(serializers.ModelSerializer):
    """Serializer for Leaderboard model"""
    user = UserSerializer(read_only=True)
    team = TeamSerializer(read_only=True)
    
    class Meta:
        model = Leaderboard
        fields = [
            'id', 'leaderboard_type', 'period', 'rank', 'user', 
            'team', 'points', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class AchievementSerializer(serializers.ModelSerializer):
    """Serializer for Achievement model"""
    users_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Achievement
        fields = [
            'id', 'name', 'description', 'icon_url', 'criteria',
            'users_count', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']
    
    def get_users_count(self, obj):
        return obj.users.count()


class ChallengeSerializer(serializers.ModelSerializer):
    """Serializer for Challenge model"""
    participants_count = serializers.SerializerMethodField()
    is_active = serializers.SerializerMethodField()
    
    class Meta:
        model = Challenge
        fields = [
            'id', 'name', 'description', 'start_date', 'end_date',
            'goal_points', 'participants_count', 'is_active',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_participants_count(self, obj):
        return obj.participants.count()
    
    def get_is_active(self, obj):
        return obj.is_active()
