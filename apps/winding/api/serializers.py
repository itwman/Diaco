"""
Diaco MES - Winding API Serializers (بوبین‌پیچی)
"""
from rest_framework import serializers
from apps.winding.models import Production


class WindingProductionSerializer(serializers.ModelSerializer):
    """سریالایزر کامل تولید بوبین‌پیچی."""
    status_display        = serializers.CharField(source='get_status_display',     read_only=True)
    package_type_display  = serializers.CharField(source='get_package_type_display', read_only=True)
    machine_code          = serializers.CharField(source='machine.code',            read_only=True)
    line_code             = serializers.CharField(source='production_line.code',    read_only=True, default=None)
    operator_name         = serializers.SerializerMethodField()
    waste_pct             = serializers.FloatField(read_only=True)
    quality_grade         = serializers.CharField(read_only=True)

    class Meta:
        model  = Production
        fields = '__all__'

    def get_operator_name(self, obj):
        return obj.operator.get_full_name() if obj.operator else None


class WindingProductionListSerializer(serializers.ModelSerializer):
    """سریالایزر سبک برای لیست (فقط فیلدهای ضروری)."""
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    machine_code   = serializers.CharField(source='machine.code',       read_only=True)
    quality_grade  = serializers.CharField(source='quality_grade',      read_only=True)

    class Meta:
        model  = Production
        fields = [
            'id', 'batch_number', 'production_date',
            'machine_code', 'status', 'status_display',
            'output_weight_kg', 'cuts_per_100km', 'efficiency_pct',
            'quality_grade',
        ]
