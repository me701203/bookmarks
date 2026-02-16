from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Image


class ImageLikeTest(TestCase):
    def setUp(self):
        # 1. Create a fake user for testing
        self.user = User.objects.create_user(username="testuser", password="password")

        # 2. Create a fake image record in the database
        self.image = Image.objects.create(
            user=self.user, title="Test Image", slug="test-image", image="test.jpg"
        )
        # 3. Setup the simulated browser (Client)
        self.client = Client()
        self.client.login(username="testuser", password="password")

    def test_like_action(self):
        # 4. Tell the "Robot" to send a POST request to the 'like' view
        url = reverse("images:like")
        response = self.client.post(
            url,
            {"id": self.image.id, "action": "like"},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )

        # 5. Check if the server responded with "OK" (Status 200)
        self.assertEqual(response.status_code, 200)

        # 6. Check the database: Is the user actually in the 'users_like' list now?
        self.assertIn(self.user, self.image.users_like.all())
