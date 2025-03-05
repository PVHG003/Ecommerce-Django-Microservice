import logging
import re

import cloudinary.uploader
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import ItemModel
from .serializers import BookSerializer, SmartphoneSerializer, FashionSerializer, BaseItemSerializer

cloudinary.config(
    cloud_name=settings.CLOUDINARY_CLOUD_NAME,
    api_key=settings.CLOUDINARY_API_KEY,
    api_secret=settings.CLOUDINARY_API_SECRET,  # Click 'View API Keys' above to copy your API secret
    secure=True
)


def get_serializer_by_category(category):
    category = category.lower()
    if category == "books":
        return BookSerializer
    elif category == "mobiles":
        return SmartphoneSerializer
    elif category in ["fashions"]:
        return FashionSerializer
    return BaseItemSerializer


# Create your views here.
class AddItemView(APIView):
    def post(self, request):
        try:
            data = request.data
            category = data.get("category", "").lower()
            if not category:
                return Response({"error": "Invalid category"}, status=status.HTTP_400_BAD_REQUEST)
            serializer_class = get_serializer_by_category(category)
            serializer = serializer_class(data=data)

            if not serializer.is_valid():
                return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

            image_urls = []
            if "images" in request.FILES:
                uploaded_images = request.FILES.getlist("images")
                for image in uploaded_images:
                    upload_result = cloudinary.uploader.upload(image, folder=f"assets/{category}")
                    image_urls.append(upload_result["secure_url"])

            serializer.validated_data["image_urls"] = image_urls
            item_id = ItemModel.create_item(serializer.validated_data)

            return Response({"item_id": item_id}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ItemListView(APIView):
    def get(self, request):
        items = ItemModel.get_all_items()
        for item in items:
            item["_id"] = str(item["_id"])
        return Response({"items": items}, status=status.HTTP_200_OK)


class ItemDetailView(APIView):
    def get(self, request, item_id):
        logging.warning(item_id)
        item = ItemModel.get_item(item_id)
        logging.warning(item)
        if item:
            item["_id"] = str(item["_id"])
            return Response(item, status=status.HTTP_200_OK)
        return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, item_id):
        data = request.data

        if "images" in request.FILES:
            image_urls = []
            uploaded_images = request.FILES.getlist("images")
            for image in uploaded_images:
                upload_result = cloudinary.uploader.upload(image)
                image_urls.append(upload_result["secure_url"])
            data["image_urls"] = image_urls

        ItemModel.update_item(item_id, data)
        return Response({"item_id": item_id}, status=status.HTTP_200_OK)

    def delete(self, request, item_id):
        logging.warning(item_id)
        item = ItemModel.get_item(item_id)
        logging.warning(item)
        for image_url in item["image_urls"]:
            logging.warning(image_url)
            match = re.search(r"/v\d+/(.+)\.\w+$", image_url)
            if match:
                public_id = match.group(1)
                cloudinary.uploader.destroy(public_id)
                logging.warning(public_id)
        ItemModel.delete_item(item_id)
        return Response({"success": "true"}, status=status.HTTP_200_OK)


class SearchItemView(APIView):
    def get(self, request):
        query = request.GET.get("query", "")
        items = ItemModel.search_items({"name": {"$regex": query, "$options": "i"}})
        for item in items:
            item["_id"] = str(item["_id"])
        return Response({"items": items}, status=status.HTTP_200_OK)


class FilterItemView(APIView):
    def get(self, request, category):
        items = ItemModel.filter_by_category(category)
        for item in items:
            item["_id"] = str(item["_id"])
        return Response({"items": items}, status=status.HTTP_200_OK)
