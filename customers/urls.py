from django.urls import path

from customers.views import CustomerBalanceAPIView, CustomerListCreateAPIView, CustomerRetrieveAPIView

urlpatterns = [
    path('', CustomerListCreateAPIView.as_view(), name='customer-list-create'),
    path('<str:external_id>/', CustomerRetrieveAPIView.as_view(), name='customer-retrieve'),
    path('<str:external_id>/balance/', CustomerBalanceAPIView.as_view(), name='customer-balance-retrieve'),
]
