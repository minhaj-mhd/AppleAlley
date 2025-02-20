from django import forms
from .models import Address, Customer

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ["street_address","locality","city","state","pincode","landmark"]

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ["first_name", "last_name", "phone"]
        