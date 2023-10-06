from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.core.validators import MaxValueValidator, MinValueValidator


class UserManager(BaseUserManager):
    "Custom user model manager"

    def create_user(self, email, password, **other):
        if not email:
            raise ValueError("Email must be provided")
        email = self.normalize_email(email)
        user = self.model(email=email, **other)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **other):
        user = self.create_user(email, password, **other)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    "Custom user model"
    email = models.EmailField(max_length=50, unique=True, blank=False)
    username = models.CharField(max_length=50, blank=False)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateField(auto_now_add=True)
    objects = UserManager()

    USERNAME_FIELD = "email"

    def __str__(self):
        return "@{}".format(self.username)


class Product(models.Model):
    """Model for representing products."""

    name = models.CharField(max_length=255)
    description = models.TextField(max_length=10000)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    image = models.ImageField(upload_to="products", null=True, blank=True)


class Review(models.Model):
    """Product reviews. One to many relationship."""

    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="reviews")
    product = models.ForeignKey(
        "Product", on_delete=models.CASCADE, related_name="reviews"
    )
    rating = models.IntegerField(
        validators=[MaxValueValidator(5), MinValueValidator(1)]
    )
    description = models.TextField(max_length=10000)
