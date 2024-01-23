from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework_api_key.models import APIKey
from customers.models import Customer
from loans.models import Loan
from model_bakery import baker

class LoansAPITestCase(APITestCase):
    def setUp(self):
        _, key = APIKey.objects.create_key(name="test")
        self.authorization = f"Api-Key {key}"

    def test_view_response_without_api_key(self):
        url = reverse('loan-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_view_response_with_api_key(self):
        url = reverse('loan-list-create')
        response = self.client.get(url, HTTP_AUTHORIZATION=self.authorization)
        self.assertEqual(response.status_code, 200)

    def test_view_get_loan_list(self):
        url = reverse('loan-list-create')
        baker.make(Loan, _quantity=10)
        response = self.client.get(url, HTTP_AUTHORIZATION=self.authorization)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 10)

    def test_view_create_loan_accept(self):
        url = reverse('loan-list-create')
        baker.make(Customer, external_id="pepe", score="101.00")
        data = {
            "external_id": "loan_pepe",
            "customer_external": 'pepe',
            "amount": "100"
        }
        response = self.client.post(url, data=data, HTTP_AUTHORIZATION=self.authorization)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data.get('outstanding'), '100.00')

    def test_view_create_loan_declined(self):
        url = reverse('loan-list-create')
        baker.make(Customer, external_id="pepe", score="99.00")
        data = {
            "external_id": "loan_pepe",
            "customer_external": 'pepe',
            "amount": "100.00"
        }
        response = self.client.post(url, data=data, HTTP_AUTHORIZATION=self.authorization)
        self.assertEqual(response.status_code, 400)

    def test_view_get_loan_customer(self):
        customer = baker.make(Customer, external_id="pepe", score="120.00")
        url = reverse('loan-customer-list', kwargs={'customer_external': customer.external_id})
        baker.make(Loan, amount='1.00', _quantity=3, customer_external=customer)
        baker.make(Loan, amount='1.00', _quantity=5)
        response = self.client.get(url, HTTP_AUTHORIZATION=self.authorization)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 3)

    def test_view_change_status_2(self):
        loan = baker.make(Loan, status=1, external_id="loan_test")
        url = reverse('loan-status-update', kwargs={'external_id': loan.external_id})
        data = {
            "status": 2
        }
        response = self.client.put(url, data=data, HTTP_AUTHORIZATION=self.authorization)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('status'), 2)

    def test_view_change_status_3(self):
        loan = baker.make(Loan, status=1, external_id="loan_test")
        url = reverse('loan-status-update', kwargs={'external_id': loan.external_id})
        data = {
            "status": 3
        }
        response = self.client.put(url, data=data, HTTP_AUTHORIZATION=self.authorization)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('status'), 3)

    def test_view_change_status_4(self):
        loan = baker.make(Loan, status=1, external_id="loan_test")
        url = reverse('loan-status-update', kwargs={'external_id': loan.external_id})
        data = {
            "status": 4
        }
        response = self.client.put(url, data=data, HTTP_AUTHORIZATION=self.authorization)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data.get('status')[0].code, 'invalid')


    def test_view_change_sequence(self):
        loan = baker.make(Loan, status=1, external_id="loan_test")
        url = reverse('loan-status-update', kwargs={'external_id': loan.external_id})
        data = {
            "status": 2
        }
        response = self.client.put(url, data=data, HTTP_AUTHORIZATION=self.authorization)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('status'), 2)
        data = {
            "status": 3
        }
        response = self.client.put(url, data=data, HTTP_AUTHORIZATION=self.authorization)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data.get('status')[0].code, 'invalid')
