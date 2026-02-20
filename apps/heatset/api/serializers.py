"""
Diaco MES - HeatSet API Serializers (هیت‌ست)
"""
from rest_framework import serializers
from apps.heatset.models import Batch, CycleLog


class CycleLogSerializer(serializers.ModelSerializer):
    """سریالایزر لاگ چرخه — AI Time Series Data."""
    phase_display = serializers.CharField(source='get_phase_display', read_only=True)

    class Meta:
        model  = CycleLog
        fields = [
            'id', 'elapsed_min', 'log_time',
            'temperature_c', 'pressure_bar', 'humidity_pct',
            'phase', 'phase_display', 'created_at',
        ]


class HeatsetBatchSerializer(serializers.ModelSerializer):
    """سریالایزر کامل بچ هیت‌ست."""
    status_display          = serializers.CharField(source='get_status_display',            read_only=True)
    quality_result_display  = serializers.CharField(source='get_quality_result_display',    read_only=True)
    machine_type_hs_display = serializers.CharField(source='get_machine_type_hs_display',   read_only=True)
    fiber_type_display      = serializers.CharField(source='get_fiber_type_display',        read_only=True)
    twist_stability_display = serializers.CharField(source='get_twist_stability_display',   read_only=True)
    machine_code            = serializers.CharField(source='machine.code',                  read_only=True)
    line_code               = serializers.CharField(source='production_line.code',          read_only=True, default=None)
    operator_name           = serializers.SerializerMethodField()
    is_passed               = serializers.BooleanField(read_only=True)
    cycle_logs              = CycleLogSerializer(many=True, read_only=True)

    class Meta:
        model  = Batch
        fields = '__all__'

    def get_operator_name(self, obj):
        return obj.operator.get_full_name() if obj.operator else None


class HeatsetBatchListSerializer(serializers.ModelSerializer):
    """سریالایزر سبک برای لیست."""
    status_display         = serializers.CharField(source='get_status_display',          read_only=True)
    quality_result_display = serializers.CharField(source='get_quality_result_display',  read_only=True)
    machine_code           = serializers.CharField(source='machine.code',                read_only=True)

    class Meta:
        model  = Batch
        fields = [
            'id', 'batch_number', 'production_date',
            'machine_code', 'machine_type_hs', 'fiber_type',
            'temperature_c', 'duration_min', 'batch_weight_kg',
            'status', 'status_display',
            'quality_result', 'quality_result_display',
            'shrinkage_pct', 'twist_stability',
        ]
