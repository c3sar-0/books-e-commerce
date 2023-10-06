from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from core.models import Product, Review


P1 = {
    "name": "asd",
    "description": "asdasd",
    "stock": 5,
    "price": 12.5,
}
R1 = {
    "description": "good product",
    "rating": 4,
}


def get_review_list_url(pk):
    return "/api/products/{}/reviews/".format(pk)


def get_review_detail_url(p_pk, r_pk):
    return "/api/products/{}/reviews/{}/".format(p_pk, r_pk)


class PublicProductsAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()


class PrivateProductsAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create(
            username="test", email="test@example.com"
        )
        self.client.force_authenticate(self.user)

    def test_create_review_succ(self):
        product = Product.objects.create(**P1)

        res = self.client.post(get_review_list_url(product.pk), R1)

        self.assertEqual(res.status_code, 201)

    def test_delete_review_succ(self):
        product = Product.objects.create(**P1)
        review = Review.objects.create(**R1, user=self.user, product=product)

        res = self.client.delete(get_review_detail_url(product.pk, review.pk))

        self.assertEqual(res.status_code, 204)
        self.assertNotIn(review, product.reviews.all())
