from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient


USERS_URL = reverse("users:users")
ME_URL = reverse("users:me")
TOKEN_PAIR_URL = reverse("users:token_obtain_pair")
TOKEN_REFRESH_URL = reverse("users:token_refresh")
P1 = {
    "email": "asd@example.com",
    "username": "asd",
    "password": "12312312",
}
P2 = {
    "username": "asd2",
    "email": "asd2@example.com",
    "password": "32132132",
}
P3 = {
    "username": "asd3",
    "email": "asd3@example.com",
    "password": "12341234",
}


def create_user(username="asd", email="asd@example.com", password="12312312"):
    "Create and return a new user"
    return get_user_model().objects.create(
        username=username, email=email, password=password
    )


class PublicUsersAPITests(TestCase):
    """Test the public features of the users api"""

    def setUp(self):
        self.client = APIClient()

    def test_create_user_succ(self):
        """Test creating a user is successful"""
        payload = P1
        res = self.client.post(USERS_URL, payload)

        self.assertEqual(res.status_code, 201)
        user = get_user_model().objects.get(email=payload["email"])
        self.assertTrue(user.check_password(payload["password"]))
        self.assertNotIn("password", res.data)


class PrivateUsersAPITests(TestCase):
    """Test the private features of the users api"""

    def setUp(self):
        self.user = create_user(username="test", email="test@example.com")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_update_user_succ(self):
        """Test updating a user is successful"""
        res = self.client.put(ME_URL, P2)
        user = self.user

        self.assertEqual(res.status_code, 200)
        user.refresh_from_db()
        self.assertEqual(user.username, P2["username"])
        self.assertEqual(user.email, P2["email"])
        self.assertTrue(user.check_password(P2["password"]))
