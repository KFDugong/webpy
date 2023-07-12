from django.db import models
from django.db.models import Avg

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to="product_images/")
    manual = models.FileField(
        upload_to="product_manuals/", null=True, blank=True
    )  # PDF files

    def average_rating(self):
        from reviews.models import Rating
        avg = Rating.objects.filter(product=self).aggregate(Avg('rating'))['rating__avg']
        if avg is None:
            return 0
        return avg