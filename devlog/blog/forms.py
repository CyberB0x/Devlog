from django import forms
from .models import Article
from django.contrib.auth.forms import AuthenticationForm
from .models import Comment


class BootstrapLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'image']
        widgets = {
            'title': forms.TextInput(attrs={"class": "form-control"}),
            'image': forms.ClearableFileInput(attrs={"class": "form-control"}),
        }


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
