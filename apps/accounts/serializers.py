"""
Accounts Serializers: User, Address
"""
from rest_framework import serializers
from .models import CustomUser, Address


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'phone',
                  'user_type', 'loyalty_points', 'lifetime_value', 'date_joined']
        read_only_fields = ['id', 'username', 'user_type', 'loyalty_points', 'lifetime_value', 'date_joined']


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'address_type', 'is_default', 'full_name', 'phone',
                  'country', 'region', 'city', 'district', 'street_address', 'postal_code']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'phone']

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)
