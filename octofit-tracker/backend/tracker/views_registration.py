"""Custom registration view for Djongo compatibility"""
from dj_rest_auth.registration.views import RegisterView
from rest_framework import status
from rest_framework.response import Response
from .serializers_registration import DjangoMongoDBRegisterSerializer


class DjangoMongoDBRegisterView(RegisterView):
    """Custom registration view that avoids Djongo ObjectId issues"""
    serializer_class = DjangoMongoDBRegisterSerializer
    
    def perform_create(self, serializer):
        """Skip email setup that causes ObjectId issues"""
        user = serializer.save(self.request)
        return user
