from django.db.models import Sum
from decimal import Decimal
from loans.models import Loan
from customers.models import Customer

def get_customer_balance(customer_external_id):
    customer = Customer.objects.get(external_id=customer_external_id)
    total_debt = Loan.objects.filter(customer_external=customer, status__in=[1, 2]).aggregate(total_debt=Sum('outstanding'))['total_debt'] or Decimal('0.0')
    available_amount = customer.score - total_debt

    return {
        'external_id': customer.external_id,
        'score': customer.score,
        'total_debt': total_debt,
        'available_amount': available_amount
    }
