from rest_framework import serializers
from django.contrib.auth import get_user_model


class UserDetailSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField(max_length=50)
    password = serializers.CharField(min_length=8, write_only=True)

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if password:
            instance.set_password(password)
            instance.save()

        return instance


class UserListSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=50)
