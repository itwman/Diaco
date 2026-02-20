from rest_framework import serializers
from apps.blowroom.models import Batch, BatchInput


class BatchInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = BatchInput
        fields = '__all__'


class BlowroomBatchSerializer(serializers.ModelSerializer):
    inputs = BatchInputSerializer(source='batch_inputs', many=True, read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    line_code = serializers.CharField(source='production_line.code', read_only=True, default=None)

    class Meta:
        model = Batch
        fields = '__all__'
