from django.db import models
import uuid
from django.db.models import PROTECT
from customers.models import Customer
from django.forms import ValidationError
from django.utils import timezone

class Loan(models.Model):
    STATUS_CHOICES = (
        (1, 'Pending'),
        (2, 'Active'),
        (3, 'Rejected'),
        (4, 'Paid'),
    )
    external_id = models.CharField(max_length=60, unique=True, default=uuid.uuid4, primary_key=True)
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

    def validate_loan(self, customer, amount_paid):
        if self.status == 1:
            raise ValidationError(f'Loan {self.external_id} is pending.')
        if self.customer_external != customer:
            raise ValidationError(f'Load not is that -> {customer.external_id}')
        if amount_paid > self.outstanding:
            raise ValidationError(f'Paid bigger than load -> {self.external_id}')

    def paid_loan(self, amount_paid):
        if amount_paid <= self.outstanding:
            self.outstanding = self.outstanding - amount_paid
            if self.outstanding == 0:
                self.status = 4
                self.paid_at = timezone.now()
            self.save()