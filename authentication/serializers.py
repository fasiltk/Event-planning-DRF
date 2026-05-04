from rest_framework import serializers
from .models import Authentication


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Authentication
        fields = ['name', 'email', 'password', 'role']


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()