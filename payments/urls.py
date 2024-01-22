from django.urls import path
from payments.views import PaymentCreateAPIView, PaymentListByCustomerAPIView

urlpatterns = [
    path('', PaymentCreateAPIView.as_view(), name='payment-create'),
    path('<str:customer>/', PaymentListByCustomerAPIView.as_view(), name='payment-customer-list'),
]