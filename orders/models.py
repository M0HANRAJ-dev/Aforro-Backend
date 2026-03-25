from django.db import models
from store.models import Store
from products.models import Product

class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING'
        CONFIRMED = 'CONFIRMED'
        REJECTED = 'REJECTED'

    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='orders')
    Status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["created_at"]),
        ]

    def __str__(self):
        return f"order {self.id} - {self.Status}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity_requested = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.product.title} x {self.quantity_requested}"