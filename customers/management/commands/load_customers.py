import csv
from decimal import Decimal
from django.core.management.base import BaseCommand
from customers.models import Customer

class Command(BaseCommand):
    help = 'Load customers to file CSV'

    def add_arguments(self, parser):
        parser.add_argument('file_csv', type=str, help='CSV File')

    def handle(self, *args, **options):
        file_csv = options['file_csv']
        with open(file_csv, 'r') as archivo:
            reader = csv.DictReader(archivo)
            for row in reader:
                Customer.objects.create(
                    external_id=row['external_id'],
                    status=row['status'],
                    score=Decimal(row['score'])
                )

        self.stdout.write(self.style.SUCCESS('Customers loads finally.'))
