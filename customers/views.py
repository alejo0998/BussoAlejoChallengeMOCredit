from customers.models import Customer
from customers.serializers import CustomerModelSerializer, CustomerUpdateSerializer
from customers.services import get_customer_balance
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_api_key.permissions import HasAPIKey

class CustomerListCreateAPIView(generics.ListCreateAPIView):
    model = Customer
    queryset = Customer.objects.all()
    serializer_class = CustomerModelSerializer
    permission_classes = [HasAPIKey]

class CustomerRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerUpdateSerializer
    lookup_field = 'external_id'
    permission_classes = [HasAPIKey]

class CustomerBalanceAPIView(APIView):
    permission_classes = [HasAPIKey]
    def get(self, request, external_id):
        balance = get_customer_balance(external_id)
        return Response(balance)