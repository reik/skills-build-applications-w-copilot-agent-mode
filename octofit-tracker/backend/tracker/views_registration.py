"""Custom registration view for Djongo compatibility"""
from dj_rest_auth.registration.views import RegisterView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from dj_rest_auth.serializers import TokenSerializer
from .serializers_registration import DjangoMongoDBRegisterSerializer


class DjangoMongoDBRegisterView(RegisterView):
    """Custom registration view that avoids Djongo ObjectId issues"""
    serializer_class = DjangoMongoDBRegisterSerializer
    
    def perform_create(self, serializer):
        """Skip email setup that causes ObjectId issues"""
        user = serializer.save(self.request)
        return user

    def get_response_data(self, user):
        """Override to ensure token exists before serializing"""
        # Ensure the user has an auth token
        token, created = Token.objects.get_or_create(user=user)
        return TokenSerializer(token, context=self.get_serializer_context()).data
