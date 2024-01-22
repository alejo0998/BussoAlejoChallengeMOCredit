from customers.models import Customer
from loans.models import Loan
from rest_framework import serializers

class LoanModelSerializer(serializers.ModelSerializer):
    customer_external = serializers.CharField()
   
    class Meta:
        model = Loan
        fields = "__all__"
        read_only_fields = ('created_at', 'updated_at', 'contract_version', 'paid_at', 'status', 'outstanding', 'take_at')
   
    def create(self, validated_data):
        customer_external_id = validated_data.pop('customer_external')
        customer = Customer.objects.get(external_id=customer_external_id)
        loan = Loan.objects.create(customer_external=customer, outstanding=validated_data.get('amount'), **validated_data)
        return loan


class LoanCustomerModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = "__all__"
   

class LoanUpdateStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = ['status']

    def validate_status(self, value):
        instance = self.instance
        if instance:
            current_status = instance.status
            if value == 2 and current_status != 1:
                raise serializers.ValidationError("You cannot change the status to 'active' if it is not in 'pending'.")
            elif value == 3 and current_status != 1:
                raise serializers.ValidationError("You cannot change the status to 'rejected' if it is not in 'pending'.")
            elif value not in [2, 3]:
                raise serializers.ValidationError("Invalid status.")
        return value