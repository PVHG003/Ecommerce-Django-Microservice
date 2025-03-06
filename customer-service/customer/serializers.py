from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import Address, Customer


# Customer = get_user_model()

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["role"] = user.customer_type
        token["username"] = user.username
        token["email"] = user.email
        return token


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['house_number', 'street', 'city', 'country']


class CustomerSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='get_full_name')
    addresses = AddressSerializer(many=True, read_only=True)

    class Meta:
        model = Customer
        fields = ['email', 'full_name', 'phone', 'customer_type', 'addresses']


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    def validate(self, data):
        user = Customer.objects.filter(username=data['username']).first()
        if user is None:
            raise serializers.ValidationError("Invalid credentials")
        if not user.check_password(data['password']):
            raise serializers.ValidationError("Invalid credentials")
        return data


class RegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = Customer
        fields = ['username', 'email', 'password', 'confirm_password', 'first_name', 'last_name', 'customer_type']

    def validate_email(self, value):
        if Customer.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists")
        return value

    def create(self, validated_data):
        """Remove confirm_password and hash the password before creating a user."""
        validated_data.pop('confirm_password')  # Remove extra field
        password = validated_data.pop('password')  # Extract password

        user = Customer.objects.create(**validated_data)
        user.set_password(password)  # Hash password
        user.save()
        return user
