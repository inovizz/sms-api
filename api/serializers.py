from rest_framework import serializers
from .models import UserModel, SmsModel


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ('id', 'username', 'password')


class SmsSerializer(serializers.ModelSerializer):
    # import pdb; pdb.set_trace()

    class Meta:
        model = SmsModel
        fields = ('_from', 'to', 'text')
