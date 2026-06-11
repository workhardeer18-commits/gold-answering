from django import forms
from UMS.models.user import User


class UserProfileForm(forms.ModelForm):

    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(render_value=False),
        label="Password"
    )

    class Meta:
        model = User
        fields = ["username", "password", "phone_number", "category", 'name', 'last_name']

    def clean(self):
        cleaned_data = super().clean()

        username = cleaned_data.get("username")
        password = cleaned_data.get("password")

        if not self.instance.pk and not password:
            raise forms.ValidationError("رمز عبور الزامی است.")

        if User.objects.filter(username=username).exclude(id=self.instance.id).exists():
            raise forms.ValidationError("این نام کاربری قبلاً ثبت شده است.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)

        password = self.cleaned_data.get("password")

        # فقط اگر پسورد وارد شد تغییر کند
        if password:
            user.set_password(password)

        if commit:
            user.save()

        return user
