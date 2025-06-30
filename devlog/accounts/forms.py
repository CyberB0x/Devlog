from django import forms

class EmailForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=254)

class CodeVerificationForm(forms.Form):
    code = forms.CharField(label="Код", max_length=6)

class PasswordResetForm(forms.Form):
    new_password = forms.CharField(label="Новый пароль", widget=forms.PasswordInput)
    confirm_password = forms.CharField(label="Подтвердите пароль", widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get("new_password")
        p2 = cleaned_data.get("confirm_password")
        if p1 != p2:
            raise forms.ValidationError("Пароли не совпадают")
        return cleaned_data