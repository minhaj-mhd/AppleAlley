from django import template
from products.models import IPhoneVariant,Banner
# Register template library
register = template.Library()

@register.simple_tag
def get_featured_products(count=4):
    return IPhoneVariant.objects.all()[:count]

@register.simple_tag
def get_latest_products(count):
    return IPhoneVariant.objects.order_by("price")[:count]
@register.simple_tag
def getBanner():
    return Banner.objects.all()