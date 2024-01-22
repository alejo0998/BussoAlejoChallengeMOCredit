from django.db import models
import uuid
from customers.models import Customer

from loans.models import Loan

class Payment(models.Model):
    STATUS_CHOICES = (
        (1, 'Completed'),
        (2, 'Rejected'),
    )
    external_id = models.CharField(max_length=60, unique=True, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    paid_at = models.DateTimeField(null=True)
    payments_loans_detail = models.ManyToManyField('PaymentLoanDetail', related_name='payments_loans')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='customer_payment')


class PaymentLoanDetail(models.Model):
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name='payment_detail')
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE, related_name='loan_detail')
    amount_paid_for_loan = models.DecimalField(max_digits=12, decimal_places=2)

    def update_loan(self):
        amount_paid = self.amount_paid_for_loan
        self.loan.update_amount(amount_paid)