from django import forms

from OMS.models.product import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'can_buy_online', 'can_sell_online']
