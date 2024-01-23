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
    payments_loans_detail = models.ManyToManyField('PaymentLoanDetail', related_name='payments_loans')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='customer_payment')
    rejection_reason = models.CharField(max_length=50, null=True)

    def handle_rejection(self, reason):
        self.status = 2
        self.rejection_reason = reason
        self.save()

    def handle_create_payments_loans_detail(self, payments_loans_detail, exception=False):
        payment_loan_details = []
        for detail_data in payments_loans_detail:
            payment_detail = PaymentLoanDetail.objects.create(payment=self, **detail_data)
            payment_loan_details.append(payment_detail)
        self.payments_loans_detail.set(payment_loan_details)
        self.save()
    
    def handle_paid_loans(self):
        for payment_detail in self.payments_loans_detail.all():
            payment_detail.loan.paid_loan(payment_detail.amount_paid_for_loan)


class PaymentLoanDetail(models.Model):
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name='payment_detail')
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE, related_name='loan_detail')
    amount_paid_for_loan = models.DecimalField(max_digits=12, decimal_places=2)
