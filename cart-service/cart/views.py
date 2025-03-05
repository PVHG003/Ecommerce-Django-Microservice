import json
import logging

import requests
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from .serializers import CartSerializer, CartItemSerializer
from .models import Cart, CartItem


def fetch_product_api(appended_url: str = ""):
    url = f'http://product:8000/api/{appended_url}/'
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        logging.warning(json.dumps(data, indent=4, ensure_ascii=False))
        return data
    except requests.RequestException as e:
        logging.warning({"error": str(e)})
        return None


# Create your views here.
class AddItemToCartView(APIView):

    def post(self, request):
        token = request.headers.get("Authorization").split(" ")[1]
        logging.warning(token)

        user_id = request.user.id
        item_id = request.data.get("item_id")
        quantity = request.data.get("quantity", 1)

        item = fetch_product_api(f"items/{item_id}")
        if not item:
            return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)

        cart, _ = Cart.objects.get_or_create(user_id=user_id)

        cart_item_data = {
            "cart": cart.id,
            "item_id": item_id,
            "item": item,
            "quantity": quantity,
        }

        serializer = CartItemSerializer(data=cart_item_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # return Response("error", status=status.HTTP_400_BAD_REQUEST)
