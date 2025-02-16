from django import template
from products.models import Product,Banner
# Register template library
register = template.Library()

@register.simple_tag
def get_featured_products(count=4):
    return Product.objects.order_by("priority")[:count]

@register.simple_tag
def get_latest_products(count):
    return Product.objects.order_by("-created_at")[:count]
@register.simple_tag
def getBanner():
    return Banner.objects.get(id=1)
    