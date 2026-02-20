from rest_framework import serializers
from apps.maintenance.models import Schedule, WorkOrder, DowntimeLog, MachineServiceDate


class ScheduleSerializer(serializers.ModelSerializer):
    is_overdue = serializers.BooleanField(read_only=True)

    class Meta:
        model = Schedule
        fields = '__all__'


class WorkOrderSerializer(serializers.ModelSerializer):
    total_cost = serializers.DecimalField(max_digits=15, decimal_places=0, read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = WorkOrder
        fields = '__all__'


class DowntimeLogSerializer(serializers.ModelSerializer):
    reason_display = serializers.CharField(source='get_reason_category_display', read_only=True)

    class Meta:
        model = DowntimeLog
        fields = '__all__'


class MachineServiceDateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MachineServiceDate
        fields = '__all__'
