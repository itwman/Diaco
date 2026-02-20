from rest_framework import serializers
from apps.passage.models import Production, Input


class PassageInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Input
        fields = '__all__'


class PassageProductionSerializer(serializers.ModelSerializer):
    inputs = PassageInputSerializer(source='passage_inputs', many=True, read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    passage_display = serializers.CharField(source='get_passage_number_display', read_only=True)
    line_code = serializers.CharField(source='production_line.code', read_only=True, default=None)

    class Meta:
        model = Production
        fields = '__all__'
