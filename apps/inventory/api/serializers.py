from rest_framework import serializers
from apps.inventory.models import FiberCategory, FiberStock, DyeStock, ChemicalStock, StockTransaction


class FiberCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = FiberCategory
        fields = '__all__'


class FiberStockSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    consumed_pct = serializers.FloatField(read_only=True)

    class Meta:
        model = FiberStock
        fields = '__all__'


class DyeStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = DyeStock
        fields = '__all__'


class ChemicalStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChemicalStock
        fields = '__all__'


class StockTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockTransaction
        fields = '__all__'
