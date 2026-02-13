"""Custom registration serializer for Djongo compatibility"""
from dj_rest_auth.registration.serializers import SocialLoginSerializer, RegisterSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class DjangoMongoDBRegisterSerializer(RegisterSerializer):
    """Custom register serializer that avoids Djongo ObjectId issues"""
    
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password1', 'password2')

    def create(self, validated_data):
        """Override create to skip email setup that causes ObjectId issues"""
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password1']
        )
        return user
