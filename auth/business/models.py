from django.db import models
from authApp.models import *
from django.conf import settings
from django.utils import timezone
import datetime
from cloudinary_storage.storage import RawMediaCloudinaryStorage




class MyCloudinaryStorage(RawMediaCloudinaryStorage):
    folder = "property/images"

# Create your models here.
class Property(models.Model):
    CHOICES = (
        ('Real Asset', 'Real Asset'),
        ('Real Banking', 'Real Banking'),
        ('Real Project', 'Real Project'),

    )

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    property_name = models.CharField(max_length=255, null=True)
    category = models.CharField(max_length=200, choices= CHOICES, null=True)
    duration = models.DecimalField(null=True, max_digits=10, decimal_places=2)
    roi = models.DecimalField(null=True, max_digits=5, decimal_places=2)
    price_per_slot = models.DecimalField(null=True, max_digits=15, decimal_places=2)
    location = models.CharField(max_length=300, null=True)
    amount = models.CharField(max_length=255, null=True)
    image1 = models.ImageField(upload_to='images/', null=True, blank=True, storage=MyCloudinaryStorage())
    image2 = models.ImageField(upload_to='images/', null=True, blank=True, storage=MyCloudinaryStorage())
    image3 = models.ImageField(upload_to='images/', null=True, blank=True, storage=MyCloudinaryStorage())
    slots_available = models.DecimalField(null=True, max_digits=10, decimal_places=2)
    description = models.TextField(null=True, blank=True)
    terms_and_condition = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.property_name

    class Meta:
        verbose_name_plural = "Property"