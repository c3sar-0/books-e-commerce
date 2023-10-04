from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


app_name = "users"

urlpatterns = [
    path("", views.UserListView.as_view(), name="user-list"),
    path("<int:pk>/", views.UserDetailView.as_view(), name="user-detail"),
    path("me/", views.MeView.as_view(), name="me"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
