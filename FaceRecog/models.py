# Create your models here.
import datetime

from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.
class Customer(models.Model):
    id = models.UUIDField(default=uuid.uuid4().hex, primary_key=True)
    contract = models.CharField(max_length=10, unique=True, null=False)
    name = models.CharField(max_length=100, null=True)
    phone_number = models.CharField(max_length=11, null=False)
    email = models.CharField(max_length=100, null=False)
    created_datetime = models.DateTimeField(auto_now_add=True)