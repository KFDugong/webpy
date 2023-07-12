from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from products.models import Product
from .models import Comment, Rating


class ReviewViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.product = Product.objects.create(
            name="Test Product", description="Test Description", price=10
        )
        self.comment = Comment.objects.create(
            user=self.user, product=self.product, text="Test comment"
        )
        self.rating = Rating.objects.create(
            user=self.user, product=self.product, rating=3
        )
        self.client.login(username="testuser", password="12345")

    def test_comment_detail_view(self):
        response = self.client.get(
            reverse("reviews:comment_detail", args=[self.comment.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test comment")

    def test_comment_update_view(self):
        response = self.client.post(
            reverse("reviews:comment_update", args=[self.comment.id]),
            {"text": "Updated comment"},
        )
        self.comment.refresh_from_db()
        self.assertEqual(self.comment.text, "Updated comment")

    def test_comment_delete_view(self):
        response = self.client.post(
            reverse("reviews:comment_delete", args=[self.comment.id])
        )
        self.assertEqual(Comment.objects.filter(id=self.comment.id).exists(), False)

    def test_rating_detail_view(self):
        response = self.client.get(
            reverse("reviews:rating_detail", args=[self.rating.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "3")

    def test_rating_update_view(self):
        response = self.client.post(
            reverse("reviews:rating_update", args=[self.rating.id]), {"rating": 5}
        )
        self.rating.refresh_from_db()
        self.assertEqual(self.rating.rating, 5)

    def test_rating_delete_view(self):
        response = self.client.post(
            reverse("reviews:rating_delete", args=[self.rating.id])
        )
        self.assertEqual(Rating.objects.filter(id=self.rating.id).exists(), False)

    def test_comment_feedback_view(self):
        response = self.client.get(
            reverse("reviews:comment_feedback", args=[self.comment.id, 1])
        )
        self.comment.refresh_from_db()
        self.assertEqual(self.comment.feedback, 1)

    def test_comment_toggle_hidden_view(self):
        response = self.client.get(
            reverse("reviews:comment_toggle_hidden", args=[self.comment.id])
        )
        self.comment.refresh_from_db()
        self.assertEqual(self.comment.is_hidden, True)

    def test_comment_detail_view(self):
        response = self.client.get(
            reverse("reviews:comment_detail", args=[self.comment.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test comment")

    def test_comment_update_view(self):
        response = self.client.post(
            reverse("reviews:comment_update", args=[self.comment.id]),
            {"text": "Updated comment"},
        )
        self.comment.refresh_from_db()
        self.assertEqual(self.comment.text, "Updated comment")

    def test_comment_delete_view(self):
        response = self.client.post(
            reverse("reviews:comment_delete", args=[self.comment.id])
        )
        self.assertEqual(Comment.objects.filter(id=self.comment.id).exists(), False)

    def test_rating_detail_view(self):
        response = self.client.get(
            reverse("reviews:rating_detail", args=[self.rating.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "3")

    def test_rating_update_view(self):
        response = self.client.post(
            reverse("reviews:rating_update", args=[self.rating.id]), {"rating": 5}
        )
        self.rating.refresh_from_db()
        self.assertEqual(self.rating.rating, 5)

    def test_rating_delete_view(self):
        response = self.client.post(
            reverse("reviews:rating_delete", args=[self.rating.id])
        )
        self.assertEqual(Rating.objects.filter(id=self.rating.id).exists(), False)

    def test_comment_feedback_view(self):
        response = self.client.get(
            reverse("reviews:comment_feedback", args=[self.comment.id, 1])
        )
        self.comment.refresh_from_db()
        self.assertEqual(self.comment.feedback, 1)

    def test_comment_toggle_hidden_view(self):
        response = self.client.get(
            reverse("reviews:comment_toggle_hidden", args=[self.comment.id])
        )
        self.comment.refresh_from_db()
        self.assertEqual(self.comment.is_hidden, True)
