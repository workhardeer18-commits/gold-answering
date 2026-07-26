from django import forms

from OMS.models.product import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['zaryar_id', 'zaryar_title', 'title', 'can_buy_online', 'can_sell_online']
