from customers.models import Customer
from loans.models import Loan
from payments.models import Payment
from payments.serializers import PaymentModelSerializer, PaymentRetrieveSerializer
from rest_framework import generics
from rest_framework.response import Response
from rest_framework_api_key.permissions import HasAPIKey
from rest_framework.exceptions import ValidationError
from decimal import Decimal

class PaymentCreateAPIView(generics.CreateAPIView):
    model = Payment
    queryset = Payment.objects.all()
    serializer_class = PaymentModelSerializer
    permission_classes = [HasAPIKey]

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data, context={'request': request})
            serializer.is_valid(raise_exception=True)
            payment = serializer.save()
            payment.handle_paid_loans()
            return Response(self.serializer_class(payment).data, status=201)
        except ValidationError as ve:
            customer = Customer.objects.get(external_id=request.data.pop('customer_external_id'))
            payments_loans_detail = request.data.pop('payments_loans_detail')
            total_amount = sum(Decimal(item['amount_paid_for_loan']) for item in payments_loans_detail)
            instance = Payment.objects.create(status=2, customer=customer, total_amount=total_amount, **request.data)
            loan_ids = [item['loan'] for item in payments_loans_detail]
            loan_objects = Loan.objects.in_bulk(loan_ids)
            payments_loans_detail_with_objects = [
                {'loan': loan_objects[item['loan']], 'amount_paid_for_loan': item['amount_paid_for_loan']}
                for item in payments_loans_detail
            ]
            instance.handle_create_payments_loans_detail(payments_loans_detail_with_objects)
            instance.handle_rejection(str(ve))
            return Response(self.serializer_class(instance).data, status=201)

class PaymentListByCustomerAPIView(generics.ListAPIView):
    model = Payment
    serializer_class = PaymentRetrieveSerializer
    permission_classes = [HasAPIKey]

    def get_queryset(self):
        customer_external = self.kwargs.get('customer')
        payments = Payment.objects.filter(customer__external_id=customer_external)
        return payments