from django.contrib.auth.models import User
from django.forms import ModelForm
from models import *
from django.forms import widgets
class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        widgets = {
            'password': forms.PasswordInput(),
        }


class CustomerForm(ModelForm):
    class Meta:
        model = Customers
        fields = ('location', 'name')

class MerchantForm(ModelForm):
    class Meta:
        model = Merchants
        fields = ('location', 'name','cost')

from django import forms
class DocumentForm(forms.Form):
    docfile = forms.FileField(
        label='Select a file'
    )

class OrderForm(ModelForm):
    # docfile = forms.FileField(
    #     label='Select a file'
    # )
    # qty=forms.IntegerField()
    # date_of_order=forms.DateField()
    # date_of_delivery=forms.DateField()
    # customer = forms.ModelMultipleChoiceField(queryset=Customers.objects.all())
    # merchant = forms.ModelMultipleChoiceField(queryset=Merchants.objects.all())
    class Meta:
        model = Orders
        fields = ('qty','docfile')
        exclude=('customer','completed','merchant','date_of_order',)