from django.db import models

# Create your models here.
class Product(models.Model):
    LIVE = 1
    DELETE = 0
    DELETE_CHOICES = ((LIVE,"Live"),(DELETE,"Delete"))
    title = models.CharField(max_length=200)
    brand = models.CharField(max_length=200,null=True)
    price = models.FloatField()
    description = models.TextField()
    image = models.ImageField(upload_to="media/")
    priority = models.IntegerField(default=0)
    deleted_status = models.IntegerField(choices=DELETE_CHOICES,default=0 )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return self.brand + " " + self.title
    
class Banner(models.Model):
    image = models.ImageField(upload_to="media/",null=True)
    heading = models.CharField(max_length=400)
    description = models.CharField(max_length=600)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    
    

class IPhoneSeries(models.Model):
    name = models.CharField(max_length=50, unique=True)
    release_year = models.IntegerField(blank=True, null=True)

    class Meta:
        verbose_name = "iPhone Series"
        verbose_name_plural = "iPhone Series"

    def __str__(self):
        return self.name
class IPhoneModel(models.Model):
    series = models.ForeignKey(IPhoneSeries, on_delete=models.CASCADE, related_name='models')
    name = models.CharField(max_length=50)
    display_size = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    release_date = models.DateField(blank=True, null=True)
    # Removed storage_options and color_options


    def __str__(self):
        return f"{self.series.name} {self.name}"

class StorageOption(models.Model):
    capacity = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.capacity

class ColorOption(models.Model):
    color_name = models.CharField(max_length=30, unique=True)
    color_hex = models.CharField(max_length=7, blank=True, null=True)

    def __str__(self):
        return self.color_name

class IPhoneVariant(models.Model):
    model = models.ForeignKey(IPhoneModel, on_delete=models.CASCADE, related_name='variants')
    storage = models.ForeignKey(StorageOption, on_delete=models.CASCADE)
    color = models.ForeignKey(ColorOption, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.PositiveIntegerField(default=0)
    refurbished = models.BooleanField(default=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='iphone_images/', blank=True, null=True)

    class Meta:
        unique_together = ('model', 'storage', 'color')

    def __str__(self):
        return f"{self.model} - {self.storage} - {self.color}"
