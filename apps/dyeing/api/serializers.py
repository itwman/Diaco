from rest_framework import serializers
from apps.dyeing.models import Batch, ChemicalUsage, BoilerLog, DryerLog


class ChemicalUsageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChemicalUsage
        fields = '__all__'


class DyeingBatchSerializer(serializers.ModelSerializer):
    chemical_usages = ChemicalUsageSerializer(many=True, read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    line_code = serializers.CharField(source='production_line.code', read_only=True, default=None)

    class Meta:
        model = Batch
        fields = '__all__'


class BoilerLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoilerLog
        fields = '__all__'


class DryerLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = DryerLog
        fields = '__all__'
