from django import forms
from .models import Seller

class SellerCreationForm(forms.ModelForm):
    class Meta:
        model = Seller
        fields = ['name','address','phone_number','role']