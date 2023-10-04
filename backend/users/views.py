from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import (
    IsAuthenticated,
)
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import UserDetailSerializer, UserListSerializer
from core.models import User


class UserListView(APIView):
    "View for listing and creating users: POST, GET"

    def get(self, request):
        serializer = UserListSerializer(instance=User.objects.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = UserDetailSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetailView(APIView):
    """Detail view for retrieving users."""

    def get(self, request, pk):
        user = User.objects.get(pk=pk)
        serializer = UserDetailSerializer(instance=user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MeView(APIView):
    """View for managing authenticated user: PUT, DELETE"""

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        serializer = UserDetailSerializer(instance=request.user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        serializer = UserDetailSerializer(instance=request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request):
        request.user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
