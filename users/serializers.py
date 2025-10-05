from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    # password2 is a write-only field for password confirmation[cite: 107].
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']
        extra_kwargs = {
            # The password field is write-only to prevent it from being sent in API responses[cite: 108].
            'password': {'write_only': True}
        }

    # Object-level validation to ensure passwords match[cite: 111].
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    # Overriding create to use the create_user method, which correctly handles password hashing[cite: 109, 110].
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user