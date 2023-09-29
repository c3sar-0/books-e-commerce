from rest_framework import serializers
from django.contrib.auth import get_user_model


class UserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField(max_length=50)
    password = serializers.CharField(min_length=8, write_only=True)

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)
