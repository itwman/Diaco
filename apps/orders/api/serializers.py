from rest_framework import serializers
from apps.orders.models import Customer, ColorShade, Order


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'


class ColorShadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ColorShade
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='customer.name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    priority_display = serializers.CharField(source='get_priority_display', read_only=True)
    line_code = serializers.CharField(source='production_line.code', read_only=True, default=None)

    class Meta:
        model = Order
        fields = '__all__'
