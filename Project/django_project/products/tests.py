from django.test import TestCase, Client
from django.urls import reverse
from .models import Product
from django.contrib.auth.models import User, Permission


def create_sample_product(
    name="Test Product", description="Test Description", price=100.00
):
    return Product.objects.create(name=name, description=description, price=price)


class ProductModelTests(TestCase):
    def test_product_creation(self):
        product = create_sample_product()
        self.assertEqual(Product.objects.count(), 1)


class ProductViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.product = create_sample_product()
        self.user = User.objects.create_user(
            "testuser", "test@test.com", "testpassword"
        )
        add_product = Permission.objects.get(codename="add_product")
        change_product = Permission.objects.get(codename="change_product")
        delete_product = Permission.objects.get(codename="delete_product")
        self.user.user_permissions.add(add_product)
        self.user.user_permissions.add(change_product)
        self.user.user_permissions.add(delete_product)
        self.client.login(username="testuser", password="testpassword")

    def test_product_list_view(self):
        response = self.client.get(reverse("products:product_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Product")

    def test_product_delete_view(self):
        response = self.client.post(
            reverse("products:product_delete", args=[self.product.id])
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Product.objects.count(), 0)

    def test_product_list_view(self):
        response = self.client.get(reverse("products:product_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product.name)
        self.assertContains(response, self.product.description)
        self.assertContains(response, self.product.price)

    def test_product_create_view(self):
        response = self.client.get(reverse("products:product_create"))
        self.assertEqual(response.status_code, 200)

    def test_product_update_view(self):
        response = self.client.get(
            reverse("products:product_update", args=[self.product.id])
        )
        self.assertEqual(response.status_code, 200)

    def test_product_delete_view(self):
        response = self.client.get(
            reverse("products:product_delete", args=[self.product.id])
        )
        self.assertEqual(response.status_code, 200)

    def test_product_delete_post(self):
        response = self.client.post(
            reverse("products:product_delete", args=[self.product.id])
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Product.objects.count(), 0)
