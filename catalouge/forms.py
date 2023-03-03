from django import forms
from .models import Product, Category

class ProductCreationForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'autofocus': 'autofocus'}))

    class Meta:
        model = Product
        exclude = ('seller','shop')

    def __init__(self, *args, **kwargs):
        super(ProductCreationForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        shop = kwargs['initial']['shop']
        self.fields['category'].queryset = Category.objects.filter(shop=shop)