from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

class UserProfile(models.Model):
    """Extended user profile with fitness-related information"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.URLField(blank=True, null=True)
    fitness_level = models.CharField(
        max_length=20,
        choices=[
            ('beginner', 'Beginner'),
            ('intermediate', 'Intermediate'),
            ('advanced', 'Advanced'),
        ],
        default='beginner'
    )
    date_of_birth = models.DateField(blank=True, null=True)
    total_points = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-total_points']

    def __str__(self):
        return f"{self.user.username} - {self.total_points} points"


class ActivityType(models.Model):
    """Types of activities that can be logged"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    base_points_per_unit = models.IntegerField(default=10)  # Points per unit (e.g., per km for running)
    unit = models.CharField(
        max_length=20,
        choices=[
            ('km', 'Kilometers'),
            ('miles', 'Miles'),
            ('minutes', 'Minutes'),
            ('reps', 'Repetitions'),
        ],
        default='minutes'
    )
    
    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Activity(models.Model):
    """User activity logs"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    activity_type = models.ForeignKey(ActivityType, on_delete=models.SET_NULL, null=True)
    distance_or_duration = models.FloatField(validators=[MinValueValidator(0)])
    calories_burned = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    points_earned = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    description = models.TextField(blank=True)
    logged_at = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-logged_at']
        indexes = [
            models.Index(fields=['user', '-logged_at']),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.activity_type} on {self.logged_at}"


class Team(models.Model):
    """Team for competitive challenges"""
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='teams_created')
    members = models.ManyToManyField(User, related_name='teams')
    total_points = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-total_points']

    def __str__(self):
        return self.name

    def calculate_total_points(self):
        """Calculate total points from all team members"""
        total = 0
        for member in self.members.all():
            if hasattr(member, 'profile'):
                total += member.profile.total_points
        self.total_points = total
        self.save()
        return total


class Leaderboard(models.Model):
    """Leaderboard rankings"""
    LEADERBOARD_TYPE_CHOICES = [
        ('individual', 'Individual'),
        ('team', 'Team'),
    ]
    
    PERIOD_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('all_time', 'All Time'),
    ]

    leaderboard_type = models.CharField(max_length=20, choices=LEADERBOARD_TYPE_CHOICES)
    period = models.CharField(max_length=20, choices=PERIOD_CHOICES, default='weekly')
    rank = models.IntegerField(validators=[MinValueValidator(1)])
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='leaderboard_entries')
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, blank=True)
    points = models.IntegerField(validators=[MinValueValidator(0)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['rank']
        indexes = [
            models.Index(fields=['leaderboard_type', 'period', 'rank']),
        ]
        unique_together = [
            ('leaderboard_type', 'period', 'rank'),
            ('user', 'leaderboard_type', 'period'),
        ]

    def __str__(self):
        entity = self.user.username if self.user else self.team.name
        return f"{entity} - Rank {self.rank} ({self.period})"


class Achievement(models.Model):
    """Achievement badges users can earn"""
    name = models.CharField(max_length=100)
    description = models.TextField()
    icon_url = models.URLField(blank=True, null=True)
    criteria = models.JSONField(default=dict)  # JSON definition of criteria
    users = models.ManyToManyField(User, related_name='achievements', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Challenge(models.Model):
    """Monthly or special fitness challenges"""
    name = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    goal_points = models.IntegerField(validators=[MinValueValidator(1)])
    participants = models.ManyToManyField(User, related_name='challenges')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-start_date']

    def __str__(self):
        return self.name

    def is_active(self):
        now = timezone.now()
        return self.start_date <= now <= self.end_date
