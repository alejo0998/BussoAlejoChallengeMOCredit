from django.db import models
import uuid
from django.db.models import PROTECT
from django.utils import timezone
from customers.models import Customer


class Loan(models.Model):
    STATUS_CHOICES = (
        (1, 'Pending'),
        (2, 'Active'),
        (3, 'Rejected'),
        (4, 'Paid'),
    )
    external_id = models.CharField(max_length=60, unique=True, default=uuid.uuid4)
    customer_external = models.ForeignKey(Customer, null=False, on_delete=PROTECT, related_name="customer_loan")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    outstanding = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    paid_at = models.DateTimeField(null=True)
    contract_version = models.CharField(max_length=30)
    maximus_payment_date = models.DateTimeField(auto_now=True)
    take_at = models.DateTimeField(null=True)

    def update_amount(self, amount_paid):
        if amount_paid > self.outstanding:
            self.status = 4
            self.save()
            raise Exception()
        self.outstanding = self.outstanding - amount_paid
        if self.outstanding == 0:
            self.status = 4
            self.paid_at = timezone.now()
        self.save()