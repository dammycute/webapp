from django.db import models
from authApp.models import *
# from uuidfield import UUIDField


# Create your models here.

class NinModel(models.Model):
    customer = models.ForeignKey(CustomerDetails, on_delete=models.CASCADE)
    is_verified = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=255)

    def __str__(self):
        return self.transaction_id

class BvnModel(models.Model):
    customer = models.ForeignKey(CustomerDetails, on_delete=models.CASCADE)
    is_verified = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=255)

    def __str__(self):
        return self.transaction_id