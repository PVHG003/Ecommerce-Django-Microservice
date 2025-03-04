from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models


class Customer(AbstractUser):
    CUSTOMER_TYPES = [
        ('regular', 'Regular Customer'),
        ('premium', 'Premium Customer'),
        ('seller', 'Seller'),
        ('admin', 'Admin'),
    ]

    phone = models.CharField(max_length=20)
    customer_type = models.CharField(choices=CUSTOMER_TYPES, default='regular', max_length=10)
    groups = models.ManyToManyField(Group, related_name="customer_users", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="customer_permissions", blank=True)



class Address(models.Model):
    ADDRESS_TYPES = [
        ('home', 'Home'),
        ('work', 'Work'),
        ('other', 'Other')
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="addresses")
    house_number = models.CharField(max_length=20)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    address_type = models.CharField(choices=ADDRESS_TYPES, default='home', max_length=10)

    def __str__(self):
        return f"{self.street}, {self.city}, {self.country}"
