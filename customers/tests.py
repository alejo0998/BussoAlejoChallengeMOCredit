from customers.models import Customer
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework_api_key.models import APIKey
from loans.models import Loan
from model_bakery import baker

class CustomersAPITestCase(APITestCase):
    def setUp(self):
        _, key = APIKey.objects.create_key(name="test")
        self.authorization = f"Api-Key {key}"

    def test_view_response_without_api_key(self):
        url = reverse('customer-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_view_response_with_api_key(self):
        url = reverse('customer-list-create')
        response = self.client.get(url, HTTP_AUTHORIZATION=self.authorization)
        self.assertEqual(response.status_code, 200)

    def test_view_post(self):
        url = reverse('customer-list-create')
        data = {
            "external_id": "test_pepe",
            "status": 1,
            "score": "100"
        }
        response = self.client.post(url, data=data, HTTP_AUTHORIZATION=self.authorization)
        self.assertEqual(response.status_code, 201)
        customers = Customer.objects.all()
        self.assertEqual(customers[0].external_id, "test_pepe")

    def test_view_post_with_same_external_id(self):
        url = reverse('customer-list-create')
        data = {
            "external_id": "test_pepe",
            "status": 1,
            "score": "100"
        }
        response = self.client.post(url, data=data, HTTP_AUTHORIZATION=self.authorization)
        self.assertEqual(response.status_code, 201)
        customers = Customer.objects.all()
        self.assertEqual(customers[0].external_id, "test_pepe")
        data = {
            "external_id": "test_pepe",
            "status": 1,
            "score": "1000"
        }
        response = self.client.post(url, data=data, HTTP_AUTHORIZATION=self.authorization)
        self.assertEqual(response.status_code, 400)

    def test_view_get_list(self):
        url = reverse('customer-list-create')
        baker.make(Customer, _quantity=5)
        response = self.client.get(url, HTTP_AUTHORIZATION=self.authorization)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 5)

    def test_view_get_retrieve(self):
        customer = baker.make(Customer, external_id="pepe", score="1000.00")
        url = reverse('customer-get-retrieve', kwargs={'external_id': customer.external_id})
        response = self.client.get(url, HTTP_AUTHORIZATION=self.authorization)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('score'), '1000.00')

    def test_view_get_retrieve_balance(self):
        customer = baker.make(Customer, external_id="pepe", score="1000.00")
        baker.make(Loan, customer_external=customer, amount=50, outstanding=50, status=2)
        baker.make(Loan, customer_external=customer, amount=435, outstanding=400, status=2)
        url = reverse('customer-balance-retrieve', kwargs={'external_id': customer.external_id})
        response = self.client.get(url, HTTP_AUTHORIZATION=self.authorization)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('total_debt'), 450)
        self.assertEqual(response.data.get('available_amount'), 550)
