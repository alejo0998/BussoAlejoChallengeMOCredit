from loans.models import Loan
from loans.serializers import LoanModelSerializer
from payments.models import Payment, PaymentLoanDetail
from rest_framework import serializers
from django.utils import timezone


class PaymentLoanDetailSerializer(serializers.ModelSerializer):
    loan_external_id = serializers.CharField(write_only=True, source='loan.external_id', required=True)
    class Meta:
        model = PaymentLoanDetail
        fields = ['loan_external_id', 'loan', 'amount_paid_for_loan']
        read_only_fields = ('loan',)

class PaymentModelSerializer(serializers.ModelSerializer):
    payments_loans_detail = PaymentLoanDetailSerializer(many=True)

    class Meta:
        model = Payment
        fields = "__all__"
        read_only_fields = ('created_at', 'updated_at', 'status', 'paid_at', 'total_amount')

    def create(self, validated_data):
        try:
            payments_loans_detail_data = validated_data.pop('payments_loans_detail')
            payment = Payment.objects.create(**validated_data, total_amount=0)
            amount_paid_for_loan_list = []
            payment_loan_details = []
            for detail_data in payments_loans_detail_data:
                loan_external_id = detail_data.pop('loan').get('external_id')
                loan = Loan.objects.get(external_id=loan_external_id, customer_external=payment.customer)
                detail = PaymentLoanDetail.objects.create(payment=payment, loan=loan, **detail_data)
                detail.update_loan()
                amount_paid_for_loan_list.append(detail.amount_paid_for_loan)
                payment_loan_details.append(detail)
            total_amount = sum(amount_paid_for_loan_list)
            payment.total_amount = total_amount
            payment.payments_loans_detail.set(payment_loan_details)
            payment.paid_at = timezone.now()
            self.save()
            payment.save()
            return payment
        except Exception:
            payment.status = 2
            payment.save()
            return payment


class PaymentRetrieveSerializer(serializers.ModelSerializer):
    payments_loans_detail = PaymentLoanDetailSerializer(many=True)

    class Meta:
        model = Payment
        fields = "__all__"
