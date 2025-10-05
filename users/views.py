from rest_framework import generics, permissions
from .serializers import UserRegistrationSerializer

class UserRegistrationView(generics.CreateAPIView):
    """
    API view for user registration. Allows any user to sign up.
    """
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny] # No authentication required for signup.