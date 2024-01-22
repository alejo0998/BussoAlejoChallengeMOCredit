from customers.models import Customer
from rest_framework import serializers

class CustomerModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = "__all__"
        read_only_fields = ('created_at', 'updated_at')


class CustomerUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = "__all__"
        read_only_fields = ('created_at', 'updated_at', 'preaproved_at')

