from django import forms
from UMS.models.user_category import UserCategory


class UserCategoryForm(forms.ModelForm):
    class Meta:
        model = UserCategory
        fields = '__all__'
