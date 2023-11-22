from core.models import Product, Review
from .serializers import (
    ProductListSerializer,
    ProductDetailSerializer,
    ReviewSerializer,
)

from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Custom permission to only allow owners of an object to edit it."""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user == obj.user


class ProductListView(APIView):
    """Product list view. GET"""

    def get(self, request):
        serializer = ProductListSerializer(Product.objects.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductDetailView(APIView):
    """Product detail view. GET"""

    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductDetailSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ReviewListView(APIView):
    """Product review list view. GET POST"""

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    authentication_classes = [JWTAuthentication]

    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        serializer = ReviewSerializer(product.reviews.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, pk):
        product = Product.objects.get(pk=pk)
        serializer = ReviewSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user=request.user, product=product)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReviewDetailView(APIView):
    """Product review detail view. GET PUT DELETE"""

    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    authentication_classes = [JWTAuthentication]

    def get(self, request, product_pk, review_pk):
        review = get_object_or_404(Review, pk=review_pk)
        serializer = ReviewSerializer(review)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, product_pk, review_pk):
        review = get_object_or_404(Review, pk=review_pk)
        self.check_object_permissions(request, review)
        serializer = ReviewSerializer(instance=review, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, product_pk, review_pk):
        review = Review.objects.get(pk=review_pk)
        self.check_object_permissions(request, review)
        review.delete()
        return Response({}, status=status.HTTP_204_NO_CONTENT)
