from django.contrib import admin
from .models import Product,Banner,IPhoneModel,IPhoneSeries,StorageOption,ColorOption,IPhoneVariant
# Register your models here.
admin.site.register(Product)
admin.site.register(Banner)
admin.site.register(IPhoneSeries)
admin.site.register(StorageOption)
admin.site.register(ColorOption)
admin.site.register(IPhoneModel)
admin.site.register(IPhoneVariant)