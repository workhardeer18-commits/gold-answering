from django import forms
from OMS.models.category_product_mazaneh import CategoryProductMazaneh


class CategoryProductMazanehForm(forms.ModelForm):
    class Meta:
        model = CategoryProductMazaneh
        fields = ['category', 'product', 'buy_mazaneh', 'sell_mazaneh']

        # استایل‌دهی به فیلدها (اختیاری - برای ظاهر بهتر در UI)
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'product': forms.Select(attrs={'class': 'form-control'}),
            'buy_mazaneh': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'مظنه خرید'}),
            'sell_mazaneh': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'مظنه فروش'}),
        }

        labels = {
            'category': 'دسته‌بندی کاربر',
            'product': 'محصول',
            'buy_mazaneh': 'مظنه خرید',
            'sell_mazaneh': 'مظنه فروش',
        }
