from django import forms
from .models import Seller, Branch

class SellerCreationForm(forms.ModelForm):
    class Meta:
        model = Seller
        fields = ['name','address','phone_number','role']
    def __init__(self, *args, **kwargs):
        super(SellerCreationForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        

class BranchCreationForm(forms.ModelForm):
    class Meta:
        model = Branch
        fields = ['name','address','mobileNumber','address2','city','pincode']

    def __init__(self, *args, **kwargs):
        super(BranchCreationForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        
