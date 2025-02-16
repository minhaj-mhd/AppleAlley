from django import template
from products.models import Product
from orders.models import Order,OrderItem
# Register template library
register = template.Library()

@register.simple_tag
def multiply(a,b):
    return(a*b)


@register.simple_tag
def getSubTotal(cart):
    total=0
    for obj in cart.cart.all():
        total = obj.product.price * obj.quantity+total
    return total

@register.simple_tag        
def tax(subtotal):
    return subtotal*.18

@register.simple_tag        
def getTotal(subTotal,tax):
    return subTotal+tax
