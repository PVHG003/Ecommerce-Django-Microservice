from rest_framework import serializers

from .models import Cart, CartItem


class CartItemSerializer(serializers.ModelSerializer):
    total_price = serializers.FloatField(read_only=True, default=0.0)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = CartItem
        fields = ["id", "cart", "item_id", "item", "quantity", "total_price", "created_at", "updated_at", ]


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)  # Nested items inside cart
    total = serializers.FloatField(read_only=True, default=0.0)

    class Meta:
        model = Cart
        fields = ["id", "user_id", "created_at", "updated_at", "items", "total"]
