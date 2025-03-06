import json
import logging

import requests
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Cart, CartItem
from .serializers import CartItemSerializer


def fetch_product_api(appended_url: str = ""):
    url = f'http://product:8000/api/{appended_url}/'
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        logging.warning(json.dumps(data, indent=4, ensure_ascii=False))
        return data.get("data")
    except requests.RequestException as e:
        logging.warning({"error": str(e)})
        return None


class CartItemView(APIView):

    def post(self, request):
        try:
            user_id = request.user.id
            item_id = request.data.get("item_id")
            quantity = request.data.get("quantity", 1)

            if not item_id:
                return Response({"success": False, "message": "Item ID is required."},
                                status=status.HTTP_400_BAD_REQUEST)

            item = fetch_product_api(f"items/{item_id}")
            if not item:
                return Response({"success": False, "message": "Item not found."},
                                status=status.HTTP_404_NOT_FOUND)

            cart, _ = Cart.objects.get_or_create(user_id=user_id)

            cart_item, created = CartItem.objects.get_or_create(cart=cart, item_id=item_id, defaults={
                "item": item,
                "quantity": quantity
            })

            if not created:
                cart_item.quantity += quantity
                cart_item.total_price = cart_item.item.get("price") * cart_item.quantity
                cart_item.save()

            return Response({"success": True, "message": "Item added to cart.",
                             "data": CartItemSerializer(cart_item).data}, status=status.HTTP_200_OK)

        except Exception as e:
            logging.error(str(e))
            return Response({"success": False, "message": "Error adding item to cart.", "error": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request):
        try:
            user_id = request.user.id
            cart, _ = Cart.objects.get_or_create(user_id=user_id)
            cart_items = CartItem.objects.filter(cart=cart)
            serializer = CartItemSerializer(cart_items, many=True)

            logging.warning(serializer.data[0].get("quantity"))
            for item in serializer.data:
                total_price = item["item"].get("price", 0) * item["quantity"]
                serializer.data[serializer.data.index(item)]["total_price"] = total_price
            total = sum(item["total_price"] for item in serializer.data)

            return Response({"success": True, "message": "Cart retrieved successfully.",
                             "data": {"cart_items": serializer.data, "total": total}},
                            status=status.HTTP_200_OK)

        except Exception as e:
            logging.error(str(e))
            return Response({"success": False, "message": "Error retrieving cart.", "error": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, item_id):
        try:
            user_id = request.user.id
            cart, _ = Cart.objects.get_or_create(user_id=user_id)

            cart_item = CartItem.objects.filter(cart=cart, item_id=item_id).first()
            if not cart_item:
                return Response({"success": False, "message": "Item not found in cart."},
                                status=status.HTTP_404_NOT_FOUND)

            cart_item.quantity -= 1
            if cart_item.quantity == 0:
                cart_item.delete()
                return Response({"success": True, "message": "Item removed from cart."},
                                status=status.HTTP_200_OK)

            cart_item.save()
            return Response({"success": True, "message": "Item quantity updated.",
                             "data": CartItemSerializer(cart_item).data}, status=status.HTTP_200_OK)

        except Exception as e:
            logging.error(str(e))
            return Response({"success": False, "message": "Error removing item from cart.", "error": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ClearCartView(APIView):
    def delete(self, request):
        try:
            user_id = request.user.id
            cart, _ = Cart.objects.get_or_create(user_id=user_id)

            cart.delete()
            return Response({"success": True, "message": "Cart cleared successfully."},
                            status=status.HTTP_200_OK)

        except Exception as e:
            logging.error(str(e))
            return Response({"success": False, "message": "Error clearing cart.", "error": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
