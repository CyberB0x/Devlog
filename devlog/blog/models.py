from django.db import models
from django.contrib.auth.models import User
from markdown2 import markdown

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.CharField(max_length=200)
    content_md = models.TextField()
    content_html = models.TextField(blank=True)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    code_snippet = models.TextField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    views = models.PositiveIntegerField(default=0)


    def save(self, *args, **kwargs):
        self.content_html = markdown(self.content_md)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title



class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)


class Tip(models.Model):
    text = models.CharField(max_length=280)
    created_at = models.DateTimeField(auto_now_add=True)

class ArticleView(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    session_key = models.CharField(max_length=40)
    timestamp = models.DateTimeField(auto_now_add=True)
