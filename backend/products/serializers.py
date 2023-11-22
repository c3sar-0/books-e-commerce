from rest_framework import serializers
from core import models
from users.serializers import UserListSerializer


class ProductListSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=255)
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    stock = serializers.IntegerField()
    image = serializers.ImageField()
    rating = serializers.SerializerMethodField()

    # I don't think it's good to calculate the rating every time someone wants to get the object.
    # Maybe it should be re-calculated at the model everytime someone creates a new review
    def get_rating(self, obj):
        sum = 0
        count = 0
        for r in obj.reviews.all():
            sum += r.rating
            count += 1
        return round(sum / count)


class ProductDetailSerializer(ProductListSerializer):
    description = serializers.CharField()


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = models.Review
        fields = "__all__"
        read_only_fields = ["user", "product"]

    def get_user(self, obj):
        user = obj.user
        return UserListSerializer(user).data
