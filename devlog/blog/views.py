import json
import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Count

from .models import Article, Category, Favorite, Tip, ArticleView
from .forms import ArticleForm, RegisterForm


def home(request):
    articles = Article.objects.all().order_by('-created_at')
    return render(request, 'blog/home.html', {'articles': articles})


def article_detail(request, pk):
    article = get_object_or_404(Article, pk=pk)

    # Учёт просмотров по session_key
    session_key = request.session.session_key
    if not session_key:
        request.session.save()
        session_key = request.session.session_key

    if not ArticleView.objects.filter(article=article, session_key=session_key).exists():
        ArticleView.objects.create(article=article, session_key=session_key)
        article.views += 1
        article.save()

    # 🔢 Группируем просмотры по дням
    views = (
        ArticleView.objects
        .filter(article=article)
        .extra({'date': "DATE(timestamp)"})
        .values('date')
        .annotate(count=Count('id'))
        .order_by('date')
    )

    # 📊 Подготовка данных для графика
    chart_labels = json.dumps([str(v['date']) for v in views])
    chart_data = json.dumps([v['count'] for v in views])

    return render(request, 'blog/article_detail.html', {
        'article': article,
        'chart_labels': chart_labels,
        'chart_data': chart_data
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
def profile(request):
    user_articles = Article.objects.filter(author=request.user)
    return render(request, 'blog/profile.html', {'articles': user_articles})


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
