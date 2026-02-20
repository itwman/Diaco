from rest_framework import serializers
from apps.spinning.models import Production, TravelerReplacement


class SpinningProductionSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    line_code = serializers.CharField(source='production_line.code', read_only=True, default=None)

    class Meta:
        model = Production
        fields = '__all__'


class TravelerReplacementSerializer(serializers.ModelSerializer):
    class Meta:
        model = TravelerReplacement
        fields = '__all__'
