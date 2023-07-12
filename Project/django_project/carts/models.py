from django.db import models
from products.models import Product
from users.models import User


# Create your models here.
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    @property
    def total_price(self):
        total = 0
        for item in self.cartitem_set.all():
            total += item.total_price
        return total


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)

    @property
    def total_price(self):
        return self.product.price * self.quantity
