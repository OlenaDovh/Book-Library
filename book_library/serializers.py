from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import Book

User = get_user_model()


class BookSerializer(serializers.ModelSerializer):
    """Define the serializer for the book model."""
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Book
        fields = '__all__'
        read_only_fields = ['user', 'created_at']


class UserRegisterSerializer(serializers.ModelSerializer):
    """Define the serializer for the user model."""
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        """Create and return a new user"""
        return User.objects.create_user(**validated_data)
