from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from carts.models import Cart, CartItem
from products.models import Product

User = get_user_model()

class CartTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.client = Client()
        self.client.login(username="testuser", password="testpass")
        self.product1 = Product.objects.create(name="Product 1", price=10.00)
        self.product2 = Product.objects.create(name="Product 2", price=20.00)

    def test_add_to_cart(self):
        response = self.client.post(
            reverse("carts:add_to_cart", kwargs={"pk": self.product1.pk}),
            {"quantity": 2},
        )
        self.assertEqual(response.status_code, 302)  # Expecting a redirect
        cart = Cart.objects.get(user=self.user)
        self.assertEqual(cart.cartitem_set.count(), 1)
        cart_item = cart.cartitem_set.first()
        self.assertEqual(cart_item.product, self.product1)
        self.assertEqual(cart_item.quantity, 2)

    def test_remove_from_cart(self):
        # First add an item to cart
        self.client.post(
            reverse("carts:add_to_cart", kwargs={"pk": self.product1.pk}),
            {"quantity": 2},
        )
        cart = Cart.objects.get(user=self.user)
        self.assertEqual(cart.cartitem_set.count(), 1)

        # Now remove the item
        response = self.client.get(
            reverse("carts:remove_from_cart", kwargs={"product_id": self.product1.pk})
        )
        self.assertEqual(response.status_code, 302)  # Expecting a redirect
        self.assertEqual(cart.cartitem_set.count(), 0)

    def test_checkout(self):
        # Add items to cart
        self.client.post(
            reverse("carts:add_to_cart", kwargs={"pk": self.product1.pk}),
            {"quantity": 2},
        )
        self.client.post(
            reverse("carts:add_to_cart", kwargs={"pk": self.product2.pk}),
            {"quantity": 1},
        )
        cart = Cart.objects.get(user=self.user)
        self.assertEqual(cart.cartitem_set.count(), 2)

        # Checkout
        response = self.client.get(reverse("carts:checkout"))
        self.assertEqual(response.status_code, 302)  # Expecting a redirect
        self.assertEqual(cart.cartitem_set.count(), 0)

    def test_total_price(self):
        # Add items to cart
        self.client.post(
            reverse("carts:add_to_cart", kwargs={"pk": self.product1.pk}),
            {"quantity": 2},
        )
        self.client.post(
            reverse("carts:add_to_cart", kwargs={"pk": self.product2.pk}),
            {"quantity": 3},
        )
        cart = Cart.objects.get(user=self.user)
        self.assertEqual(cart.total_price, 2 * 10.00 + 3 * 20.00)
