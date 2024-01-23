from django.forms import ValidationError
from customers.models import Customer
from loans.models import Loan
from payments.models import Payment, PaymentLoanDetail
from rest_framework import serializers


class PaymentLoanDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentLoanDetail
        fields = ['loan', 'amount_paid_for_loan']

class PaymentModelSerializer(serializers.ModelSerializer):
    payments_loans_detail = PaymentLoanDetailSerializer(many=True)
    customer_external_id = serializers.CharField(source='customer.external_id', read_only=False)

    class Meta:
        model = Payment
        fields = "__all__"
        read_only_fields = ('created_at', 'updated_at', 'status', 'paid_at', 'total_amount', 'customer', 'rejection_reason')

    def validate(self, attrs):
        customer_external_id = attrs.get('customer').get('external_id')
        customer_external = Customer.objects.get(external_id=customer_external_id)
        loans = Loan.objects.filter(customer_external=customer_external, status=2)
        if not loans.exists():
            raise ValidationError('Not Loans active.')
        new_payments = attrs.get('payments_loans_detail')
        for new_pay in new_payments:
            loan = new_pay.get('loan')
            amount = new_pay.get('amount_paid_for_loan')
            loan.validate_loan(customer_external, amount)
        attrs['customer'] = customer_external
        return super().validate(attrs)


    def create(self, validated_data):
        payments_loans_detail_data = validated_data.pop('payments_loans_detail')
        total_amount = sum(item['amount_paid_for_loan'] for item in payments_loans_detail_data)
        payment = Payment.objects.create(**validated_data, total_amount=total_amount)
        payment.handle_create_payments_loans_detail(payments_loans_detail_data)
        return payment


class PaymentRetrieveSerializer(serializers.ModelSerializer):
    payments_loans_detail = PaymentLoanDetailSerializer(many=True)

    class Meta:
        model = Payment
        fields = "__all__"
