from rest_framework import viewsets, status, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.db.models import Sum, Q
from django.utils import timezone
from datetime import timedelta

from .models import (
    UserProfile, ActivityType, Activity, Team, 
    Leaderboard, Achievement, Challenge
)
from .serializers import (
    UserProfileSerializer, ActivityTypeSerializer, ActivitySerializer,
    TeamSerializer, LeaderboardSerializer, AchievementSerializer,
    ChallengeSerializer
)


class UserProfileViewSet(viewsets.ModelViewSet):
    """ViewSet for User Profiles"""
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_object(self):
        """Get profile for current user"""
        return self.request.user.profile
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        """Get current user's profile"""
        profile = request.user.profile
        serializer = self.get_serializer(profile)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def leaderboard(self, request):
        """Get top users by total points"""
        profiles = UserProfile.objects.all()[:10]
        serializer = self.get_serializer(profiles, many=True)
        return Response(serializer.data)


class ActivityTypeViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for Activity Types"""
    queryset = ActivityType.objects.all()
    serializer_class = ActivityTypeSerializer


class ActivityViewSet(viewsets.ModelViewSet):
    """ViewSet for Activities"""
    serializer_class = ActivitySerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['logged_at', 'points_earned']
    ordering = ['-logged_at']
    
    def get_queryset(self):
        """Return activities for current user"""
        return Activity.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        """Set current user as the activity creator"""
        activity = serializer.save(user=self.request.user)
        # Update user profile total points
        profile = self.request.user.profile
        profile.total_points += activity.points_earned
        profile.save()
    
    @action(detail=False, methods=['get'])
    def recent(self, request):
        """Get recent activities (last 7 days)"""
        seven_days_ago = timezone.now() - timedelta(days=7)
        activities = Activity.objects.filter(
            user=request.user,
            logged_at__gte=seven_days_ago
        )
        serializer = self.get_serializer(activities, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get activity statistics for current user"""
        activities = Activity.objects.filter(user=request.user)
        stats = {
            'total_activities': activities.count(),
            'total_points': activities.aggregate(Sum('points_earned'))['points_earned__sum'] or 0,
            'total_calories': activities.aggregate(Sum('calories_burned'))['calories_burned__sum'] or 0,
            'average_points_per_activity': 0,
        }
        if stats['total_activities'] > 0:
            stats['average_points_per_activity'] = stats['total_points'] / stats['total_activities']
        return Response(stats)


class TeamViewSet(viewsets.ModelViewSet):
    """ViewSet for Teams"""
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['total_points', 'created_at']
    ordering = ['-total_points']
    
    def perform_create(self, serializer):
        """Set current user as team creator and add to members"""
        team = serializer.save(created_by=self.request.user)
        team.members.add(self.request.user)
    
    @action(detail=True, methods=['post'])
    def add_member(self, request, pk=None):
        """Add a user to the team"""
        team = self.get_object()
        user_id = request.data.get('user_id')
        try:
            user = User.objects.get(id=user_id)
            team.members.add(user)
            team.calculate_total_points()
            return Response({'status': 'member added'})
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=True, methods=['post'])
    def remove_member(self, request, pk=None):
        """Remove a user from the team"""
        team = self.get_object()
        user_id = request.data.get('user_id')
        try:
            user = User.objects.get(id=user_id)
            team.members.remove(user)
            team.calculate_total_points()
            return Response({'status': 'member removed'})
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=True, methods=['get'])
    def members(self, request, pk=None):
        """Get team members with their stats"""
        team = self.get_object()
        members_data = []
        for member in team.members.all():
            profile = member.profile
            members_data.append({
                'id': member.id,
                'username': member.username,
                'total_points': profile.total_points,
                'fitness_level': profile.fitness_level,
            })
        return Response(members_data)


class LeaderboardViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for Leaderboard"""
    queryset = Leaderboard.objects.all()
    serializer_class = LeaderboardSerializer
    filter_backends = [filters.OrderingFilter]
    ordering = ['rank']
    
    def get_queryset(self):
        """Filter by leaderboard type and period"""
        leaderboard_type = self.request.query_params.get('type', 'individual')
        period = self.request.query_params.get('period', 'weekly')
        return Leaderboard.objects.filter(
            leaderboard_type=leaderboard_type,
            period=period
        )
    
    @action(detail=False, methods=['get'])
    def individual(self, request):
        """Get individual leaderboard"""
        period = request.query_params.get('period', 'weekly')
        leaderboard = Leaderboard.objects.filter(
            leaderboard_type='individual',
            period=period
        )[:10]
        serializer = self.get_serializer(leaderboard, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def teams(self, request):
        """Get team leaderboard"""
        period = request.query_params.get('period', 'weekly')
        leaderboard = Leaderboard.objects.filter(
            leaderboard_type='team',
            period=period
        )[:10]
        serializer = self.get_serializer(leaderboard, many=True)
        return Response(serializer.data)


class AchievementViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for Achievements"""
    queryset = Achievement.objects.all()
    serializer_class = AchievementSerializer
    
    @action(detail=False, methods=['get'])
    def user_achievements(self, request):
        """Get achievements for current user"""
        achievements = request.user.achievements.all()
        serializer = self.get_serializer(achievements, many=True)
        return Response(serializer.data)


class ChallengeViewSet(viewsets.ModelViewSet):
    """ViewSet for Challenges"""
    queryset = Challenge.objects.all()
    serializer_class = ChallengeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering = ['-start_date']
    
    @action(detail=False, methods=['get'])
    def active(self, request):
        """Get active challenges"""
        challenges = Challenge.objects.filter(
            start_date__lte=timezone.now(),
            end_date__gte=timezone.now()
        )
        serializer = self.get_serializer(challenges, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def join(self, request, pk=None):
        """Join a challenge"""
        challenge = self.get_object()
        challenge.participants.add(request.user)
        return Response({'status': 'joined challenge'})
    
    @action(detail=True, methods=['post'])
    def leave(self, request, pk=None):
        """Leave a challenge"""
        challenge = self.get_object()
        challenge.participants.remove(request.user)
        return Response({'status': 'left challenge'})
    
    @action(detail=True, methods=['get'])
    def participants(self, request, pk=None):
        """Get challenge participants with their progress"""
        challenge = self.get_object()
        participants_data = []
        for participant in challenge.participants.all():
            activities_points = Activity.objects.filter(
                user=participant,
                logged_at__gte=challenge.start_date,
                logged_at__lte=challenge.end_date
            ).aggregate(Sum('points_earned'))['points_earned__sum'] or 0
            
            participants_data.append({
                'id': participant.id,
                'username': participant.username,
                'points': activities_points,
                'progress_percent': (activities_points / challenge.goal_points * 100) if challenge.goal_points > 0 else 0,
            })
        return Response(sorted(participants_data, key=lambda x: x['points'], reverse=True))
