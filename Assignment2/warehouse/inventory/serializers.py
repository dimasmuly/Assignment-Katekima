from rest_framework import serializers
from .models import Item, Purchase, PurchaseDetail, Sell, SellDetail

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'code', 'name', 'unit', 'description', 'stock', 'balance', 'created_at', 'updated_at', 'is_deleted']

class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = '__all__'

class PurchaseDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseDetail
        fields = '__all__'

class SellSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sell
        fields = '__all__'

class SellDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = SellDetail
        fields = '__all__'