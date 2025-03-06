import logging
import re
import uuid

import cloudinary.uploader
from django.conf import settings
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication

from .models import ItemModel
from .serializers import BookSerializer, SmartphoneSerializer, FashionSerializer, BaseItemSerializer

cloudinary.config(
    cloud_name=settings.CLOUDINARY_CLOUD_NAME,
    api_key=settings.CLOUDINARY_API_KEY,
    api_secret=settings.CLOUDINARY_API_SECRET,
    secure=True
)


def get_serializer_by_category(category):
    category = category.lower()
    if category == "books":
        return BookSerializer
    elif category == "mobiles":
        return SmartphoneSerializer
    elif category == "fashions":
        return FashionSerializer
    return BaseItemSerializer


class AddItemView(APIView):
    authentication_classes = [JWTTokenUserAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            user = request.user

            if not user or (user.role != "seller" and not user.is_superuser):
                return Response({"success": False, "message": "Invalid seller"}, status=status.HTTP_400_BAD_REQUEST)

            data = request.data
            category = data.get("category", "").lower()
            if not category:
                return Response({"success": False, "message": "Invalid category"}, status=status.HTTP_400_BAD_REQUEST)

            serializer_class = get_serializer_by_category(category)
            serializer = serializer_class(data=data)
            if not serializer.is_valid():
                return Response({"success": False, "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

            image_urls = []
            if "images" in request.FILES:
                uploaded_images = request.FILES.getlist("images")
                for image in uploaded_images:
                    try:
                        upload_result = cloudinary.uploader.upload(
                            image,
                            public_id=f"{category}/{uuid.uuid4()}",
                            folder=f"{category}",
                            overwrite=True,
                            transfromation=[
                                {"width": 800, "height": 800, "crop": "limit", "quality": "auto"}
                            ]
                        )
                        image_urls.append(upload_result["secure_url"])
                    except Exception as e:
                        return Response({"success": False, "message": "Error uploading image", "error": str(e)},
                                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            logging.warning(user)
            serializer.validated_data["seller_id"] = str(user.id)
            serializer.validated_data["image_urls"] = image_urls
            item_id = ItemModel.create_item(serializer.validated_data)

            return Response({"success": True, "message": "Item added successfully.", "data": {"item_id": item_id}},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"success": False, "message": "Error adding item", "error": str(e)},
                            status=status.HTTP_400_BAD_REQUEST)


class ItemListView(APIView):
    def get(self, request):
        items = ItemModel.get_all_items()
        for item in items:
            item["_id"] = str(item["_id"])
        return Response({"success": True, "message": "Items retrieved successfully.", "data": {"items": items}},
                        status=status.HTTP_200_OK)


class SellerItemListView(APIView):
    authentication_classes = [JWTTokenUserAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        seller_id = request.user.id
        items = ItemModel.get_seller_items(str(seller_id))
        for item in items:
            item["_id"] = str(item["_id"])
        return Response({"success": True, "message": "Items retrieved successfully.", "data": {"items": items}},
                        status=status.HTTP_200_OK)


class ItemDetailView(APIView):

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        else:
            return [IsAuthenticated()] and [JWTTokenUserAuthentication()]

    def get(self, request, item_id):
        item = ItemModel.get_item(item_id)
        if item:
            item["_id"] = str(item["_id"])
            return Response({"success": True, "message": "Item retrieved successfully.", "data": item},
                            status=status.HTTP_200_OK)
        return Response({"success": False, "message": "Item not found"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, item_id):
        user = request.user
        item = ItemModel.get_item(item_id)

        if not item:
            return Response({"success": False, "message": "Item not found"}, status=status.HTTP_404_NOT_FOUND)

        if str(item.get("seller_id")) != str(user.id) and not user.is_superuser:
            return Response({"success": False, "message": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)

        data = request.data
        if "images" in request.FILES:
            image_urls = []
            uploaded_images = request.FILES.getlist("images")
            for image in uploaded_images:
                upload_result = cloudinary.uploader.upload(image)
                image_urls.append(upload_result["secure_url"])
            data["image_urls"] = image_urls

        ItemModel.update_item(item_id, data)
        return Response({"success": True, "message": "Item updated successfully.", "data": {"item_id": item_id}},
                        status=status.HTTP_200_OK)

    def delete(self, request, item_id):
        user = request.user
        item = ItemModel.get_item(item_id)

        if not item:
            return Response({"success": False, "message": "Item not found"}, status=status.HTTP_404_NOT_FOUND)

        if str(item.get("seller_id")) != str(user.id) and not user.is_superuser:
            return Response({"success": False, "message": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)

        for image_url in item["image_urls"]:
            match = re.search(r"/v\d+/(.+)\.\w+$", image_url)
            if match:
                public_id = match.group(1)
                cloudinary.uploader.destroy(public_id)

        ItemModel.delete_item(item_id)
        return Response({"success": True, "message": "Item deleted successfully."}, status=status.HTTP_200_OK)


class SearchItemView(APIView):
    def get(self, request):
        query = request.GET.get("query", "")
        items = ItemModel.search_items({"name": {"$regex": query, "$options": "i"}})
        for item in items:
            item["_id"] = str(item["_id"])

        return Response(
            {"success": True, "message": "Search results retrieved successfully.", "data": {"items": items}},
            status=status.HTTP_200_OK)


class FilterItemView(APIView):
    def get(self, request, category):
        items = ItemModel.filter_by_category(category)
        for item in items:
            item["_id"] = str(item["_id"])

        return Response(
            {"success": True, "message": "Filtered items retrieved successfully.", "data": {"items": items}},
            status=status.HTTP_200_OK)
