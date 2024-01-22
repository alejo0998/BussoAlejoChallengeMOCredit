from django.urls import path
from loans.views import LoanCustomerListAPIView, LoanListCreateAPIView, LoanStatusAPIView

urlpatterns = [
    path('', LoanListCreateAPIView.as_view(), name='loan-list-create'),
    path('<str:customer_external>/', LoanCustomerListAPIView.as_view(), name='loan-customer-list'),
    path('<str:external_id>/status/', LoanStatusAPIView.as_view(), name='loan-status-update'),

]