from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Address(models.Model):
    STATES_IN_INDIA = (
        ('AP', 'Andhra Pradesh'),
        ('AR', 'Arunachal Pradesh'),
        ('AS', 'Assam'),
        ('BR', 'Bihar'),
        ('CT', 'Chhattisgarh'),
        ('GA', 'Goa'),
        ('GJ', 'Gujarat'),
        ('HR', 'Haryana'),
        ('HP', 'Himachal Pradesh'),
        ('JK', 'Jammu and Kashmir'),
        ('JH', 'Jharkhand'),
        ('KA', 'Karnataka'),
        ('KL', 'Kerala'),
        ('MP', 'Madhya Pradesh'),
        ('MH', 'Maharashtra'),
        ('MN', 'Manipur'),
        ('ML', 'Meghalaya'),
        ('MZ', 'Mizoram'),
        ('NL', 'Nagaland'),
        ('OR', 'Odisha'),
        ('PB', 'Punjab'),
        ('RJ', 'Rajasthan'),
        ('SK', 'Sikkim'),
        ('TN', 'Tamil Nadu'),
        ('TS', 'Telangana'),
        ('TR', 'Tripura'),
        ('UP', 'Uttar Pradesh'),
        ('UK', 'Uttarakhand'),
        ('WB', 'West Bengal'),
        ('AN', 'Andaman and Nicobar Islands'),
        ('CH', 'Chandigarh'),
        ('DH', 'Dadra and Nagar Haveli'),
        ('DD', 'Daman and Diu'),
        ('LD', 'Lakshadweep'),
        ('DL', 'Delhi'),
        ('PY', 'Puducherry'),
    )

    # Address fields
    street_address = models.CharField(max_length=255, help_text="Street address or apartment number")
    locality = models.CharField(max_length=100, help_text="Locality or neighborhood")
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=2, choices=STATES_IN_INDIA, help_text="State in India")
    pincode = models.CharField(max_length=6, help_text="6-digit Indian Postal Code")
    landmark = models.CharField(max_length=100, null=True, blank=True, help_text="Optional landmark")

    # Additional metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.street_address}, {self.locality}, {self.city}, {self.state} - {self.pincode}'


    
class Customer(models.Model):
    LIVE = 1
    DELETE = 0
    DELETE_CHOICES = ((LIVE,"Live"),(DELETE,"Delete"))
    name = models.CharField(max_length=200)
    address = models.OneToOneField(Address,null=True,on_delete=models.SET_NULL, related_name="customer")
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name="customer")
    email_verified = models.BooleanField(default=False)
    phone = models.IntegerField()
    deleted_status = models.IntegerField(choices=DELETE_CHOICES,default=0 )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return self.name

