from django.db import models

# Create your models here.
import uuid

from django.contrib.auth.models import User
from django.db import models


class AbstractBase(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    last_updated_on = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True


class Customer(AbstractBase):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name="customer_profile")
    is_active = models.BooleanField(default=False)
    
    class Meta:
        db_table = "Customer"
        ordering = ['id']


