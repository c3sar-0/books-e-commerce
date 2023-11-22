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
R2 = {
    "description": "bad product",
    "rating": 2,
}
U1 = {
    "username": "user1",
    "email": "user1@example.com",
    "password": "passwd",
}


def get_review_list_url(pk):
    return "/api/products/{}/reviews/".format(pk)


def get_review_detail_url(p_pk, r_pk):
    return "/api/products/{}/reviews/{}/".format(p_pk, r_pk)


class PublicProductsAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_review_fail(self):
        user = get_user_model().objects.create(**U1)
        product = Product.objects.create(**P1)

        res = self.client.post(get_review_list_url(product.pk))

        self.assertEqual(res.status_code, 401)


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

    def test_update_review_succ(self):
        product = Product.objects.create(**P1)
        review = Review.objects.create(**R1, user=self.user, product=product)

        res = self.client.put(get_review_detail_url(product.pk, review.pk), data=R2)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data["description"], R2["description"])
        self.assertEqual(res.data["rating"], R2["rating"])

    def test_update_delete_others_review_fail(self):
        """Test that you can't modify or delete other users review"""
        product = Product.objects.create(**P1)
        new_user = get_user_model().objects.create(**U1)
        review = Review.objects.create(**R1, user=new_user, product=product)

        put_res = self.client.put(get_review_detail_url(product.pk, review.pk), data=R2)
        del_res = self.client.delete(get_review_detail_url(product.pk, review.pk))

        self.assertEqual(put_res.status_code, 403)
        self.assertEqual(del_res.status_code, 403)
        self.assertTrue(Review.objects.filter(pk=review.pk).exists())
