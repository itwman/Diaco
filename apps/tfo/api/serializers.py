"""
Diaco MES - TFO API Serializers (دولاتابی)
"""
from rest_framework import serializers
from apps.tfo.models import Production


class TFOProductionSerializer(serializers.ModelSerializer):
    """سریالایزر کامل تولید دولاتابی TFO."""
    status_display          = serializers.CharField(source='get_status_display',          read_only=True)
    twist_direction_display = serializers.CharField(source='get_twist_direction_display',  read_only=True)
    machine_code            = serializers.CharField(source='machine.code',                read_only=True)
    line_code               = serializers.CharField(source='production_line.code',        read_only=True, default=None)
    operator_name           = serializers.SerializerMethodField()
    waste_pct               = serializers.FloatField(read_only=True)
    calculated_output_count = serializers.FloatField(read_only=True)

    class Meta:
        model  = Production
        fields = '__all__'

    def get_operator_name(self, obj):
        return obj.operator.get_full_name() if obj.operator else None


class TFOProductionListSerializer(serializers.ModelSerializer):
    """سریالایزر سبک برای لیست."""
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    machine_code   = serializers.CharField(source='machine.code',       read_only=True)

    class Meta:
        model  = Production
        fields = [
            'id', 'batch_number', 'production_date',
            'machine_code', 'status', 'status_display',
            'ply_count', 'twist_tpm', 'twist_direction',
            'output_weight_kg', 'breakage_count', 'efficiency_pct',
        ]
