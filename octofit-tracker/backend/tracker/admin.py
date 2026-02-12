from django.contrib import admin
from .models import (
    UserProfile, ActivityType, Activity, Team,
    Leaderboard, Achievement, Challenge
)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'fitness_level', 'total_points', 'created_at']
    list_filter = ['fitness_level', 'created_at']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(ActivityType)
class ActivityTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'unit', 'base_points_per_unit']
    search_fields = ['name']


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ['user', 'activity_type', 'logged_at', 'points_earned']
    list_filter = ['activity_type', 'logged_at']
    search_fields = ['user__username', 'activity_type__name']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'logged_at'


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_by', 'total_points', 'members_count']
    list_filter = ['created_at']
    search_fields = ['name', 'created_by__username']
    readonly_fields = ['created_at', 'updated_at']
    
    def members_count(self, obj):
        return obj.members.count()
    members_count.short_description = 'Members'


@admin.register(Leaderboard)
class LeaderboardAdmin(admin.ModelAdmin):
    list_display = ['rank', 'get_entity_name', 'leaderboard_type', 'period', 'points']
    list_filter = ['leaderboard_type', 'period', 'rank']
    readonly_fields = ['created_at', 'updated_at']
    
    def get_entity_name(self, obj):
        return obj.user.username if obj.user else obj.team.name
    get_entity_name.short_description = 'Entity'


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ['name', 'users_count']
    search_fields = ['name']
    readonly_fields = ['created_at']
    
    def users_count(self, obj):
        return obj.users.count()
    users_count.short_description = 'Users'


@admin.register(Challenge)
class ChallengeAdmin(admin.ModelAdmin):
    list_display = ['name', 'start_date', 'end_date', 'goal_points', 'participants_count']
    list_filter = ['start_date', 'end_date']
    search_fields = ['name']
    readonly_fields = ['created_at', 'updated_at']
    
    def participants_count(self, obj):
        return obj.participants.count()
    participants_count.short_description = 'Participants'
