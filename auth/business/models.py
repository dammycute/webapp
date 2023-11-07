from django.db import models
from authApp.models import *
from django.conf import settings
from django.utils import timezone
import datetime




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
    image1 = models.ImageField(upload_to='images/property/', null=True, blank=True,)
    image2 = models.ImageField(upload_to='images/property/', null=True, blank=True,)
    image3 = models.ImageField(upload_to='images/property/', null=True, blank=True,)
    slots_available = models.DecimalField(null=True, max_digits=10, decimal_places=2)
    description = models.TextField(null=True, blank=True)
    terms_and_condition = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.property_name

    class Meta:
        verbose_name_plural = "Property"


class Investment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Property, null=True, on_delete=models.CASCADE)
    slots = models.PositiveBigIntegerField(null=True)
    current_value = models.DecimalField(null=True, max_digits=10, decimal_places=2)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    def calculate_roi(self, date):
        days_since_start = (date - self.start_date).days
        months_since_start = int(days_since_start / 30)
        roi = self.product.roi * months_since_start
        return roi