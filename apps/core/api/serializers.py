from rest_framework import serializers
from apps.core.models import ProductionLine, Machine, Shift, LineShiftAssignment


class ProductionLineSerializer(serializers.ModelSerializer):
    machine_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = ProductionLine
        fields = '__all__'


class LineShiftAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = LineShiftAssignment
        fields = '__all__'


class MachineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Machine
        fields = '__all__'


class MachineMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Machine
        fields = ['id', 'code', 'name', 'machine_type']


class ShiftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shift
        fields = '__all__'
