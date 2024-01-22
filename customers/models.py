from django.db import models
import uuid

# Create your models here.

class Customer(models.Model):
    STATUS_CHOICES = (
        (1, 'Active'),
        (2, 'Inactive'),
    )
    external_id = models.CharField(max_length=60, unique=True, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    score = models.DecimalField(max_digits=12, decimal_places=2)