from rest_framework import serializers
from .models import Order, Flavor

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ['user', 'status']

class FlavorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flavor
        fields = '__all__'