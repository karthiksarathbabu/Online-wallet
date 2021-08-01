import uuid

from django.db import models
from customer.models import Customer,AbstractBase


STATUS = (
    ('success', 'Success'),
    ('pending', 'Pending'),
    ('failed','Failed')
    )

TRANSACTION_TYPE = (
    ('deposit', 'Deposit'),
    ('withdrawal', 'Withdrawal')
    )

class Wallet(AbstractBase):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owned_by = models.OneToOneField(Customer,on_delete=models.CASCADE,null=True,blank=True,related_name="customer_wallet")
    balance = models.PositiveIntegerField(default=0)
    is_enabled = models.BooleanField(default=False)
    status_updated_on = models.DateField(null=True,blank=True)

    class Meta:
        db_table = "Wallet"
        ordering = ['id']


class Transactions(AbstractBase):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    wallet = models.ForeignKey(Wallet,on_delete=models.CASCADE,related_name="transactions")
    amount = models.PositiveIntegerField(default=0)
    reference_id = models.UUIDField(unique=True)
    status = models.CharField(max_length=100,choices=STATUS,default='pending')
    transaction_type = models.CharField(max_length=100,choices=TRANSACTION_TYPE)
    transacted_on = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = "Transactions"
        ordering = ['id']

