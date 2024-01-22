from customers.models import Customer
from loans.models import Loan
from loans.serializers import LoanCustomerModelSerializer, LoanModelSerializer, LoanUpdateStatusSerializer
from rest_framework import generics, status
from django.db.models import Sum
from decimal import Decimal
from rest_framework.response import Response
from django.utils import timezone
from rest_framework_api_key.permissions import HasAPIKey

class LoanListCreateAPIView(generics.ListCreateAPIView):
    model = Loan
    queryset = Loan.objects.all()
    serializer_class = LoanModelSerializer
    permission_classes = [HasAPIKey]

    def create(self, request, *args, **kwargs):
        customer_external_id = request.data.get('customer_external')
        customer = Customer.objects.get(external_id=customer_external_id)
        if customer.status == 2:
            return Response({'error': 'Customer Inactive'}, status=status.HTTP_400_BAD_REQUEST)
        score = customer.score
        loans = Loan.objects.filter(customer_external=customer)
        total_outstanding = 0
        if len(loans) > 0:
            total_outstanding = loans.aggregate(Sum('outstanding'))['outstanding__sum']
        amount = Decimal(request.data.get('amount'))
        if total_outstanding + amount > score:
            return Response({'error': 'Amount + Outstanding > Score'}, status=status.HTTP_400_BAD_REQUEST)
        return super().create(request, *args, **kwargs)


class LoanCustomerListAPIView(generics.ListAPIView):
    model = Loan
    queryset = Loan.objects.all()
    serializer_class = LoanCustomerModelSerializer
    permission_classes = [HasAPIKey]

    def get_queryset(self):
        customer_external_id = self.kwargs.get('customer_external')
        customer = Customer.objects.get(external_id=customer_external_id)
        return Loan.objects.filter(customer_external=customer)
    

class LoanStatusAPIView(generics.UpdateAPIView):
    model = Loan
    queryset = Loan.objects.all()
    serializer_class = LoanUpdateStatusSerializer
    lookup_field = 'external_id'
    permission_classes = [HasAPIKey]

    def perform_update(self, serializer):
        instance = serializer.save()
        if instance.status == 2:
            instance.take_at = timezone.now()
            instance.save()
