"""Serializers module for User and SMS models."""
from rest_framework import serializers
from .models import UserModel, SmsModel


class UserSerializer(serializers.ModelSerializer):
    """User serializer."""
    class Meta:
        model = UserModel
        fields = ('id', 'username', 'password')


class SmsSerializer(serializers.ModelSerializer):
    """SMS serializer."""
    class Meta:
        model = SmsModel
        fields = ('_from', 'to', 'text')
