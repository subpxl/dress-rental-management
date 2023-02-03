
from django import forms
from .models import  Booking
from catalouge.models import  Product


class DateInput(forms.DateInput):
    input_type = 'date'

class BookedProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name','tag']

    def __init__(self, *args, **kwargs):
        super(BookedProductForm, self).__init__(*args, **kwargs)

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        # self.queryset = Product.objects.filter()


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        exclude = ['status']
        widgets = {
            'startDate': DateInput(),
            'endDate': DateInput(),
            'products': forms.SelectMultiple,
            'amountDue':forms.TextInput(attrs={'readonly': 'readonly'})

        }
    def __init__(self, *args, **kwargs):
        super(BookingForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

