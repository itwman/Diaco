from rest_framework import serializers
from apps.accounts.models import User


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='get_full_name', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'full_name',
                  'role', 'department', 'phone', 'is_active']
        read_only_fields = ['id', 'username']


class UserMiniSerializer(serializers.ModelSerializer):
    """سریالایزر مختصر برای FK."""
    full_name = serializers.CharField(source='get_full_name', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'full_name', 'role']
