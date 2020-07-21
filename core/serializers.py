from django.contrib.auth.models import User
from rest_framework import serializers

from core.models import UserProfile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'first_name', 'last_name']


class UserProfileCreateSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = UserProfile
        fields = ['id', 'user']

    def create(self, validated_data):
        user = UserSerializer(data=validated_data.pop('user'))
        user.is_valid()
        user = user.save()
        _profile = UserProfile(**validated_data, user=user)

        return _profile
