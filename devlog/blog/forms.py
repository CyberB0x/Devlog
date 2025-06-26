from django import forms
from .models import Article
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import widgets
from django.contrib.auth.forms import AuthenticationForm
from .models import Comment, Profile

class BootstrapLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content_md', 'image', 'code_snippet', 'category']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Напишите комментарий...'
            }),
        }


class EditProfileForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput(), required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class ProfileAvatarForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar']