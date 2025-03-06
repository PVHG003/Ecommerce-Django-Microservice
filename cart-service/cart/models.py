import uuid

from django.db import models


# Create your models here.

class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.CharField(max_length=100, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class CartItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    item_id = models.CharField(max_length=100)
    item = models.JSONField()
    quantity = models.IntegerField()
    # item response example {
    #             "_id": "67c719c623a87b7f8f5af6a6",
    #             "category": "books",
    #             "name": "1",
    #             "price": 3000.0,
    #             "stock": 300,
    #             "author": "ME",
    #             "publisher": "ME 2 ME",
    #             "isbn": "1234567890",
    #             "image_urls": [
    #                 "https://res.cloudinary.com/dnugdgi2v/image/upload/v1741101506/assets/books/zsef5uxjrr9dzwsqnwwv.webp",
    #                 "https://res.cloudinary.com/dnugdgi2v/image/upload/v1741101507/assets/books/psgqvvf101u6rbbrwr0a.jpg"
    #             ]
    # }
