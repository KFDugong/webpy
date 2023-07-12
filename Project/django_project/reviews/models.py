from django.db import models
from products.models import Product
from users.models import User


# Create your models here.
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    CHOICES = [(0, "helpful"), (1, "not helpful"), (2, "inappropriate")]
    feedback = models.IntegerField(choices=CHOICES, default=0)
    is_hidden = models.BooleanField(default=False)

    def total_feedback_count(self):
        return Comment.objects.filter(
            products=self.product, feedback=self.feedback
        ).count()
    
    def toggle_hidden_status(self):
        self.is_hidden = not self.is_hidden
        self.save()
    
    def set_feedback(self, new_feedback):
        self.feedback = new_feedback
        self.save()

class Rating(models.Model):
    RATING_CHOICES = [(i, i) for i in range(6)]  # ratings from 0 to 5
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=RATING_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
