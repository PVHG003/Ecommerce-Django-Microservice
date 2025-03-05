from rest_framework import serializers


class BaseItemSerializer(serializers.Serializer):
    category = serializers.ChoiceField(choices=["books", "mobiles", "fashions"])
    name = serializers.CharField(max_length=255)
    price = serializers.FloatField(min_value=0.0)
    stock = serializers.IntegerField(min_value=0)
    image_urls = serializers.ListSerializer(
        child=serializers.URLField(), required=False, allow_empty=True
    )


class BookSerializer(BaseItemSerializer):
    author = serializers.CharField(max_length=255)
    publisher = serializers.CharField(max_length=255)
    isbn = serializers.CharField(max_length=13)
    pages = serializers.IntegerField(required=False)


class SmartphoneSerializer(BaseItemSerializer):
    brand = serializers.CharField(max_length=100)
    model = serializers.CharField(max_length=100)
    storage = serializers.CharField(max_length=50)  # Example: "128GB", "256GB"
    ram = serializers.CharField(max_length=50)  # Example: "8GB", "12GB"
    battery_capacity = serializers.IntegerField(required=False)  # in mAh


class FashionSerializer(BaseItemSerializer):
    size = serializers.CharField(max_length=10)  # S, M, L, XL, etc.
    color = serializers.CharField(max_length=50)
    material = serializers.CharField(max_length=100, required=False)
    brand = serializers.CharField(max_length=100, required=False)
