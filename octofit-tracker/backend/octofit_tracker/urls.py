"""octofit_tracker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.response import Response
from rest_framework.decorators import api_view
import os

from tracker.views import (
    UserProfileViewSet, ActivityTypeViewSet, ActivityViewSet,
    TeamViewSet, LeaderboardViewSet, AchievementViewSet, ChallengeViewSet
)
from tracker.views_registration import DjangoMongoDBRegisterView

# Create router and register viewsets
router = DefaultRouter()
router.register(r'profiles', UserProfileViewSet, basename='userprofile')
router.register(r'activity-types', ActivityTypeViewSet, basename='activitytype')
router.register(r'activities', ActivityViewSet, basename='activity')
router.register(r'teams', TeamViewSet, basename='team')
router.register(r'leaderboard', LeaderboardViewSet, basename='leaderboard')
router.register(r'achievements', AchievementViewSet, basename='achievement')
router.register(r'challenges', ChallengeViewSet, basename='challenge')

@api_view(['GET'])
def api_root(request):
    """API root endpoint"""
    codespace_name = os.environ.get('CODESPACE_NAME')
    if codespace_name:
        base_url = f"https://{codespace_name}-8000.app.github.dev"
    else:
        base_url = "http://localhost:8000"
    
    return Response({
        'message': 'Welcome to OctoFit Tracker API',
        'endpoints': {
            'profiles': f'{base_url}/api/profiles/',
            'activity-types': f'{base_url}/api/activity-types/',
            'activities': f'{base_url}/api/activities/',
            'teams': f'{base_url}/api/teams/',
            'leaderboard': f'{base_url}/api/leaderboard/',
            'achievements': f'{base_url}/api/achievements/',
            'challenges': f'{base_url}/api/challenges/',
        }
    })

urlpatterns = [
    path('', api_root, name='home'),
    path('admin/', admin.site.urls),
    path('api/', api_root, name='api-root'),
    path('api/', include(router.urls)),
    path('api/auth/', include('dj_rest_auth.urls')),
    path('api/auth/registration/', DjangoMongoDBRegisterView.as_view(), name='rest_register'),
    path('api-auth/', include('rest_framework.urls')),
]

