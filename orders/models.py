from django.db import models
from django.contrib.auth.models import User
from customers.models import Customer
from products.models import Product
# Create your models here.
class Order(models.Model):
    LIVE = 1
    DELETE = 0
    DELETE_CHOICES = ((LIVE,"Live"),(DELETE,"Delete"))
    CART_STAGE = 0
    ORDER_CONFIRMED =1
    ORDER_PROCESSING = 2
    ORDER_DELIVERED = 3
    ORDER_REJECTED = 4
    STATUS_CHOICE = ( (ORDER_CONFIRMED,"ORDER_CONFIRMED"),
                        (ORDER_PROCESSING,"ORDER_PROCESSING"),
                        (ORDER_DELIVERED,"ORDER_DELIVERED"),
                        (ORDER_REJECTED,"ORDER_REJECTED")
    )
    order_status = models.IntegerField(STATUS_CHOICE,default= CART_STAGE)
    owner = models.ForeignKey(Customer,on_delete=models.SET_NULL,null=True,related_name="order")
    deleted_status = models.IntegerField(choices=DELETE_CHOICES,default=0 )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return "order-"+self.owner.name+"  "+str(self.id)

class OrderItem(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name="order_item")
    quantity = models.IntegerField(default=1)
    order = models.ForeignKey(Order,on_delete=models.CASCADE,related_name='cart')

