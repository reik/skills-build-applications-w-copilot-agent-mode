#!/usr/bin/env python
"""
Populate the OctoFit Tracker database with test data.
Run this script from the backend directory: python populate_db.py
"""

import os
import sys
import django
from datetime import datetime, timedelta

# Setup Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'octofit_tracker.settings')
django.setup()

from django.contrib.auth.models import User
from django.utils import timezone
from tracker.models import (
    UserProfile, ActivityType, Activity, Team,
    Leaderboard, Achievement, Challenge
)


def create_activity_types():
    """Create standard activity types"""
    activity_types_data = [
        {
            'name': 'Running',
            'description': 'Outdoor or indoor running',
            'base_points_per_unit': 15,
            'unit': 'km'
        },
        {
            'name': 'Walking',
            'description': 'Casual or brisk walking',
            'base_points_per_unit': 8,
            'unit': 'km'
        },
        {
            'name': 'Cycling',
            'description': 'Cycling or stationary bike',
            'base_points_per_unit': 12,
            'unit': 'km'
        },
        {
            'name': 'Strength Training',
            'description': 'Weight training or bodyweight exercises',
            'base_points_per_unit': 2,
            'unit': 'minutes'
        },
        {
            'name': 'Yoga',
            'description': 'Yoga or pilates session',
            'base_points_per_unit': 1,
            'unit': 'minutes'
        },
        {
            'name': 'Swimming',
            'description': 'Swimming laps or recreational swimming',
            'base_points_per_unit': 20,
            'unit': 'km'
        },
    ]
    
    activity_types = []
    for data in activity_types_data:
        try:
            activity_type = ActivityType.objects.create(
                name=data['name'],
                description=data['description'],
                base_points_per_unit=data['base_points_per_unit'],
                unit=data['unit']
            )
            print(f"✓ Created activity type: {activity_type.name}")
            activity_types.append(activity_type)
        except Exception:
            # Try to get existing
            try:
                activity_type = ActivityType.objects.get(name=data['name'])
                print(f"  Activity type already exists: {activity_type.name}")
                activity_types.append(activity_type)
            except Exception as e:
                print(f"  Warning: Could not create or find {data['name']}: {e}")
    
    return activity_types


def create_test_users():
    """Create test users with profiles"""
    users_data = [
        {'username': 'alice', 'email': 'alice@example.com', 'first_name': 'Alice', 'fitness_level': 'beginner'},
        {'username': 'bob', 'email': 'bob@example.com', 'first_name': 'Bob', 'fitness_level': 'intermediate'},
        {'username': 'charlie', 'email': 'charlie@example.com', 'first_name': 'Charlie', 'fitness_level': 'advanced'},
        {'username': 'diana', 'email': 'diana@example.com', 'first_name': 'Diana', 'fitness_level': 'intermediate'},
        {'username': 'eve', 'email': 'eve@example.com', 'first_name': 'Eve', 'fitness_level': 'beginner'},
    ]
    
    users = []
    for data in users_data:
        # Check if user exists
        try:
            user = User.objects.get(username=data['username'])
            print(f"  User already exists: {user.username}")
        except User.DoesNotExist:
            user = User.objects.create_user(
                username=data['username'],
                email=data['email'],
                first_name=data['first_name'],
                password='testpass123'
            )
            print(f"✓ Created user: {user.username}")
        
        # Update profile
        if hasattr(user, 'profile'):
            user.profile.fitness_level = data['fitness_level']
            user.profile.save()
        
        users.append(user)
    
    return users


def create_activities(users, activity_types):
    """Create sample activities for users"""
    now = timezone.now()
    activities_count = 0
    
    for user in users:
        # Generate 5-10 activities per user over the last 30 days
        num_activities = 7
        for i in range(num_activities):
            activity_type = activity_types[i % len(activity_types)]
            days_ago = i * 3
            logged_at = now - timedelta(days=days_ago)
            
            # Generate random distance/duration
            if activity_type.unit == 'km':
                distance_or_duration = 5.0 + (i % 10)
            else:
                distance_or_duration = 30 + (i * 5)
            
            points_earned = int(distance_or_duration * activity_type.base_points_per_unit)
            
            try:
                activity = Activity.objects.create(
                    user=user,
                    activity_type=activity_type,
                    distance_or_duration=distance_or_duration,
                    calories_burned=100 + (i * 20),
                    points_earned=points_earned,
                    description=f'{activity_type.name} session #{i + 1}',
                    logged_at=logged_at
                )
                
                # Update user profile points
                user.profile.total_points += points_earned
                user.profile.save()
                activities_count += 1
            except Exception as e:
               # Skip if activity already exists
                pass
    
    print(f"✓ Created {activities_count} activities")


def create_teams(users):
    """Create teams with members"""
    teams_data = [
        {'name': 'Fitness Warriors', 'description': 'The hardcore fitness team', 'members': [users[0], users[1], users[2]]},
        {'name': 'Active Lifestyle', 'description': 'For those seeking a balanced active life', 'members': [users[2], users[3], users[4]]},
        {'name': 'Running Club', 'description': 'For running enthusiasts', 'members': [users[0], users[3]]},
    ]
    
    for data in teams_data:
        try:
            team = Team.objects.create(
                name=data['name'],
                description=data['description'],
                created_by=data['members'][0]
            )
            team.members.set(data['members'])
            team.calculate_total_points()
            print(f"✓ Created team: {team.name} with {team.members.count()} members")
        except Exception:
            # Team might already exist
            try:
                team = Team.objects.get(name=data['name'])
                print(f"  Team already exists: {team.name}")
            except Exception as e:
                print(f"  Warning: Could not create team {data['name']}: {e}")


def create_challenges():
    """Create fitness challenges"""
    now = timezone.now()
    challenges_data = [
        {
            'name': 'February Fitness Sprint',
            'description': 'Complete 500 points worth of activities in February',
            'start_date': now,
            'end_date': now + timedelta(days=28),
            'goal_points': 500
        },
        {
            'name': 'Running Marathon',
            'description': 'Log 100 km of running this month',
            'start_date': now,
            'end_date': now + timedelta(days=30),
            'goal_points': 1500
        },
        {
            'name': 'Strength Champion',
            'description': 'Complete 30 hours of strength training',
            'start_date': now,
            'end_date': now + timedelta(days=60),
            'goal_points': 3600
        },
    ]
    
    for data in challenges_data:
        try:
            challenge = Challenge.objects.create(
                name=data['name'],
                description=data['description'],
                start_date=data['start_date'],
                end_date=data['end_date'],
                goal_points=data['goal_points']
            )
            # Add some participants
            challenge.participants.set(User.objects.all()[:3])
            print(f"✓ Created challenge: {challenge.name}")
        except Exception:
            try:
                challenge = Challenge.objects.get(name=data['name'])
                print(f"  Challenge already exists: {challenge.name}")
            except Exception as e:
                print(f"  Warning: Could not create challenge {data['name']}: {e}")


def create_achievements():
    """Create achievement badges"""
    achievements_data = [
        {
            'name': 'First Steps',
            'description': 'Log your first activity',
            'criteria': {'activities_count': 1}
        },
        {
            'name': 'Century Club',
            'description': 'Reach 100 total points',
            'criteria': {'total_points': 100}
        },
        {
            'name': 'Running Star',
            'description': 'Complete 50 km of running',
            'criteria': {'running_km': 50}
        },
        {
            'name': 'Strength Beast',
            'description': 'Complete 50 hours of strength training',
            'criteria': {'strength_minutes': 3000}
        },
        {
            'name': 'Week Warrior',
            'description': 'Log activities 7 days in a row',
            'criteria': {'consecutive_days': 7}
        },
        {
            'name': 'Thousand Pointer',
            'description': 'Accumulate 1000 points',
            'criteria': {'total_points': 1000}
        },
    ]
    
    for data in achievements_data:
        try:
            achievement = Achievement.objects.create(
                name=data['name'],
                description=data['description'],
                criteria=data['criteria']
            )
            print(f"✓ Created achievement: {achievement.name}")
        except Exception:
            try:
                achievement = Achievement.objects.get(name=data['name'])
                print(f"  Achievement already exists: {achievement.name}")
            except Exception as e:
                print(f"  Warning: Could not create achievement {data['name']}: {e}")


def main():
    """Main function to populate the database"""
    print("\n" + "="*50)
    print("OctoFit Tracker - Database Population Script")
    print("="*50 + "\n")
    
    try:
        # Create activity types
        print("Creating Activity Types...")
        activity_types = create_activity_types()
        
        # Create test users
        print("\nCreating Test Users...")
        users = create_test_users()
        
        # Create test activities
        print("\nCreating Activities...")
        create_activities(users, activity_types)
        
        # Create teams
        print("\nCreating Teams...")
        create_teams(users)
        
        # Create challenges
        print("\nCreating Challenges...")
        create_challenges()
        
        # Create achievements
        print("\nCreating Achievements...")
        create_achievements()
        
        print("\n" + "="*50)
        print("✓ Database population completed successfully!")
        print("="*50 + "\n")
        
        # Print summary
        print("Summary:")
        print(f"  - Users: {User.objects.count()}")
        print(f"  - Activity Types: {ActivityType.objects.count()}")
        print(f"  - Activities: {Activity.objects.count()}")
        print(f"  - Teams: {Team.objects.count()}")
        print(f"  - Challenges: {Challenge.objects.count()}")
        print(f"  - Achievements: {Achievement.objects.count()}")
        print("\nTest user credentials:")
        print("  Username: alice, Password: testpass123")
        print("  Username: bob, Password: testpass123")
        print("  Username: charlie, Password: testpass123")
        print("  Username: diana, Password: testpass123")
        print("  Username: eve, Password: testpass123")
        print()
        
    except Exception as e:
        import traceback
        print(f"\n✗ Error during database population: {str(e)}")
        print("\nFull traceback:")
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
