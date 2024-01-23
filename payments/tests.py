from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework_api_key.models import APIKey
from customers.models import Customer
from loans.models import Loan
from model_bakery import baker
import json
from decimal import Decimal

class PaymentsAPITestCase(APITestCase):
    def setUp(self):
        _, key = APIKey.objects.create_key(name="test")
        self.authorization = f"Api-Key {key}"

    def test_view_response_without_api_key(self):
        url = reverse('payment-create')
        response = self.client.post(url)
        self.assertEqual(response.status_code, 403)

    def test_view_create_payment_ok(self):
        url = reverse('payment-create')
        customer = baker.make(Customer, external_id="test_create_payment", score="1000.00")
        baker.make(Loan,
                    external_id="loan_1",
                    status=2,
                    customer_external=customer, 
                    amount="100.00", 
                    outstanding="80.00")
        baker.make(Loan,
                    external_id="loan_2",
                    status=2,
                    customer_external=customer, 
                    amount="100.00", 
                    outstanding="100.00")
        data = {
            "payments_loans_detail": [
                {
                    "loan": "loan_1",
                    "amount_paid_for_loan": "80.00"
                },
                {
                    "loan": "loan_2",
                    "amount_paid_for_loan": "50.00"
                }
            ],
            "external_id": "payment_2",
            "customer_external_id": customer.external_id
            }
        response = self.client.post(url, data=json.dumps(data), content_type="application/json", HTTP_AUTHORIZATION=self.authorization, )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data.get('status'), 1)
        self.assertEqual(response.data.get('rejected_reason'), None)
        self.assertEqual(Loan.objects.get(external_id="loan_1").outstanding, Decimal('0.00'))
        self.assertEqual(Loan.objects.get(external_id="loan_1").status, 4)
        self.assertNotEqual(Loan.objects.get(external_id="loan_1").paid_at, None)
        self.assertEqual(Loan.objects.get(external_id="loan_2").outstanding, Decimal('50.00'))
        self.assertEqual(Loan.objects.get(external_id="loan_2").status, 2)
        self.assertEqual(Loan.objects.get(external_id="loan_2").paid_at, None)


    def test_view_create_payment_fail(self):
        url = reverse('payment-create')
        customer = baker.make(Customer, external_id="test_create_payment", score="1000.00")
        baker.make(Loan,
                    external_id="loan_1",
                    status=2,
                    customer_external=customer, 
                    amount="100.00", 
                    outstanding="80.00")
        baker.make(Loan,
                    external_id="loan_2",
                    status=2,
                    customer_external=customer, 
                    amount="100.00", 
                    outstanding="100.00")
        data = {
            "payments_loans_detail": [
                {
                    "loan": "loan_1",
                    "amount_paid_for_loan": "80000.00"
                },
                {
                    "loan": "loan_2",
                    "amount_paid_for_loan": "50.00"
                }
            ],
            "external_id": "payment_2",
            "customer_external_id": customer.external_id
            }
        response = self.client.post(url, data=json.dumps(data), content_type="application/json", HTTP_AUTHORIZATION=self.authorization, )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data.get('status'), 2)
        self.assertEqual(response.data.get('rejection_reason'), "{'non_field_errors': [ErrorDetail(string='Paid bigger than load -> loan_1', code='invalid')]}")
        self.assertEqual(Loan.objects.get(external_id="loan_1").outstanding, Decimal('80.00'))
        self.assertEqual(Loan.objects.get(external_id="loan_1").status, 2)
        self.assertEqual(Loan.objects.get(external_id="loan_2").outstanding, Decimal('100.00'))
        self.assertEqual(Loan.objects.get(external_id="loan_2").status, 2)


    def test_view_create_payment_fail_status_1(self):
        url = reverse('payment-create')
        customer = baker.make(Customer, external_id="test_create_payment", score="1000.00")
        baker.make(Loan,
                    external_id="loan_1",
                    status=1,
                    customer_external=customer, 
                    amount="100.00", 
                    outstanding="80.00")
        data = {
            "payments_loans_detail": [
                {
                    "loan": "loan_1",
                    "amount_paid_for_loan": "80000.00"
                }
            ],
            "external_id": "payment_2",
            "customer_external_id": customer.external_id
            }
        response = self.client.post(url, data=json.dumps(data), content_type="application/json", HTTP_AUTHORIZATION=self.authorization, )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data.get('status'), 2)
        self.assertEqual(response.data.get('rejection_reason'), "{'non_field_errors': [ErrorDetail(string='Not Loans active.', code='invalid')]}")
        self.assertEqual(Loan.objects.get(external_id="loan_1").outstanding, Decimal('80.00'))
        self.assertEqual(Loan.objects.get(external_id="loan_1").status, 1)