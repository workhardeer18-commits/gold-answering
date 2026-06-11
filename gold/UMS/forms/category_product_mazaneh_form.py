from django import forms
from OMS.models.category_product_mazaneh import CategoryProductMazaneh


class CategoryProductMazanehForm(forms.ModelForm):

    class Meta:
        model = CategoryProductMazaneh

        fields = [
            "category",
            "product",
            "mazaneh"
        ]
