from django import template
from products.models import IPhoneVariant
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
        total = obj.IPhoneVariant.price * obj.quantity+total
    return total

@register.simple_tag        
def tax(subtotal):
    return int(subtotal)*.18

@register.simple_tag        
def getTotal(subTotal,tax):
    return float(subTotal)
