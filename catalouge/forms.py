from django import forms
from .models import Product, Category

class ProductCreationForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ('branch',)

    def __init__(self, *args, **kwargs):
        super(ProductCreationForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        shop = kwargs['initial']['shop']
        self.fields['category'].queryset = Category.objects.filter(branch__main_shop=shop)