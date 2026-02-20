from rest_framework import serializers
from apps.carding.models import Production


class CardingProductionSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    line_code = serializers.CharField(source='production_line.code', read_only=True, default=None)

    class Meta:
        model = Production
        fields = '__all__'
