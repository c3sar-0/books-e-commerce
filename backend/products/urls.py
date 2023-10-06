from django.urls import path
from . import views


urlpatterns = [
    path("", views.ProductListView.as_view(), name="product-list"),
    path("<int:pk>/", views.ProductDetailView.as_view(), name="product-detail"),
    path("<int:pk>/reviews/", views.ReviewListView.as_view(), name="review-list"),
    path(
        "<int:product_pk>/reviews/<int:review_pk>/",
        views.ReviewDetailView.as_view(),
        name="review-Detail",
    ),
]
