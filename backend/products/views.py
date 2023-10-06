from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView
from core.models import Product, Review
from .serializers import (
    ProductListSerializer,
    ProductDetailSerializer,
    ReviewSerializer,
)
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly


class ProductListView(APIView):
    """Product list view. GET"""

    def get(self, request):
        serializer = ProductListSerializer(Product.objects.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductDetailView(APIView):
    """Product detail view. GET"""

    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        serializer = ProductDetailSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ReviewListView(APIView):
    """Product review list view. GET POST"""

    permission_classes = [IsAuthenticatedOrReadOnly]
    authentication_classes = [JWTAuthentication]

    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        serializer = ReviewSerializer(product.reviews.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, pk):
        product = Product.objects.get(pk=pk)
        serializer = ReviewSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user=request.user, product=product)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReviewDetailView(RetrieveAPIView):
    """Product review detail view. DELETE"""

    def delete(self, request, product_pk, review_pk):
        review = Review.objects.get(pk=review_pk)
        review.delete()
        return Response({}, status=status.HTTP_204_NO_CONTENT)
