
from django import forms
from .models import  Booking, Customer
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

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(CustomerForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        exclude = ['status','branch','seller','customer','final_paid']
        widgets = {
            'startDate': DateInput(),
            'endDate': DateInput(),
            'products': forms.SelectMultiple,
            'amountDue':forms.TextInput(attrs={'readonly': 'readonly'}),
        }
    def __init__(self, *args, **kwargs):
        super(BookingForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class BookingReturnForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields =['startDate','products','endDate','amountPaid','status','note']
        widgets = {
            'startDate': DateInput(),
            'endDate': DateInput(),
            'products': forms.SelectMultiple,
            'status':forms.TextInput(attrs={'readonly': 'readonly'}),
            'startDate': forms.TextInput(attrs={'readonly': 'readonly'}),
            'endDate': forms.TextInput(attrs={'readonly': 'readonly'}),
        }
    def __init__(self, *args, **kwargs):
        super(BookingReturnForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        booking = kwargs['initial']['booking']
        self.fields['products'].queryset = booking.products
