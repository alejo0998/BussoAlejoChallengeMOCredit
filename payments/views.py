from loans.models import Loan
from payments.models import Payment
from payments.serializers import PaymentModelSerializer, PaymentRetrieveSerializer
from rest_framework import generics
from rest_framework.response import Response
from rest_framework_api_key.permissions import HasAPIKey

class PaymentCreateAPIView(generics.CreateAPIView):
    model = Payment
    queryset = Payment.objects.all()
    serializer_class = PaymentModelSerializer
    permission_classes = [HasAPIKey]

    def create(self, request, *args, **kwargs):
        customer_external = request.data.get('customer')
        loans = Loan.objects.filter(customer_external=customer_external, status=2)
        if not loans.exists():
            return Response({'detail': 'All loans is paid.'}, status=400)
        new_payments = request.data.get('payments_loans_detail')
        for new_pay in new_payments:
            id_loan = new_pay.get('loan_external_id')
            loan = Loan.objects.get(external_id=id_loan)
            if loan.status == 1:
                return Response({'detail': f'Loan {id_loan} is pending.'}, status=400)
        return super().create(request, *args, **kwargs)

class PaymentListByCustomerAPIView(generics.ListAPIView):
    model = Payment
    serializer_class = PaymentRetrieveSerializer
    permission_classes = [HasAPIKey]

    def get_queryset(self):
        customer_external = self.kwargs.get('customer')
        payments = Payment.objects.filter(customer__external_id=customer_external)
        return payments