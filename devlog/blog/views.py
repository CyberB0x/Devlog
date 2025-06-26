from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Count

from django.db.models.functions import TruncDate
import datetime
import json

from .models import Article, Category, Favorite, Tip, ArticleView, Profile
from .forms import ArticleForm, RegisterForm, CommentForm



def home(request):
    articles = Article.objects.all().order_by('-created_at')
    return render(request, 'blog/home.html', {'articles': articles})


def article_detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    comments = article.comments.all().order_by('-created_at')

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid() and request.user.is_authenticated:
            comment = form.save(commit=False)
            comment.article = article
            comment.author = request.user
            comment.save()
            return redirect('article_detail', pk=pk)
    else:
        form = CommentForm()

    return render(request, 'blog/article_detail.html', {
        'article': article,
        'comments': comments,
        'form': form,
    })


@login_required
def add_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            return redirect('home')
    else:
        form = ArticleForm()
    return render(request, 'blog/article_form.html', {'form': form})


@login_required
def delete_article(request, pk):
    article = get_object_or_404(Article, pk=pk, author=request.user)
    article.delete()
    return redirect('home')


@login_required
def profile_view(request):
    profile = Profile.objects.get(user=request.user)
    articles = Article.objects.filter(author=request.user).order_by('-created_at')
    return render(request, 'blog/profile.html', {
        'user': request.user,
        'profile': profile,
        'articles': articles,
    })


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})


# 📊 Данные для графика просмотров (json)
def stats_view(request, pk):
    article = get_object_or_404(Article, pk=pk)
    views = (
        ArticleView.objects
        .filter(article=article)
        .extra({'date': "date(timestamp)"})
        .values('date')
        .annotate(count=Count('id'))
    )
    data = {
        'dates': [str(v['date']) for v in views],
        'views': [v['count'] for v in views]
    }
    return JsonResponse(data)
