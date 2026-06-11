from django import forms
from OMS.models.order import Order


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['amount', 'product']



