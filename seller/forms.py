from django import forms
from .models import Seller,Tax_and_Quantity

class SellerCreationForm(forms.ModelForm):
    class Meta:
        model = Seller
        fields = ['name','address','phone_number','role']
    def __init__(self, *args, **kwargs):
        super(SellerCreationForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class Tax_and_Quantity_Form(forms.ModelForm):
    class Meta:
        model=Tax_and_Quantity
        fields=["consider_tax","tax_percentage","tax_name","consider_quantity"]
        exclude=["seller"]
        

# class BranchCreationForm(forms.ModelForm):
#     class Meta:
#         model = Branch
#         fields = ['name','address','mobileNumber','address2','city','pincode']

#     def __init__(self, *args, **kwargs):
#         super(BranchCreationForm, self).__init__(*args, **kwargs)
#         for visible in self.visible_fields():
#             visible.field.widget.attrs['class'] = 'form-control'
        
