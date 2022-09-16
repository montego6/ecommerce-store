from django import forms
from django.forms import ModelForm
from .models import Category, Item, Order, Address





class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'slug']


class ItemForm(ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'title', 'image', 'description', 'category', 'quantity', 'price']


class StatusForm(ModelForm):
    class Meta:
        model = Order
        fields = ['status']


class RegisteredAddressForm(forms.ModelForm):

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['address'].queryset = Address.objects.filter(user=user)

    class Meta:
        model = Order
        fields = ['address']


class PromocodeForm(forms.Form):
    promocode = forms.CharField(max_length=20)


class OrderAddItemForm(forms.Form):
    order = forms.ModelChoiceField(queryset=Order.objects.filter(status="process"))
    quantity = forms.IntegerField(min_value=1)
