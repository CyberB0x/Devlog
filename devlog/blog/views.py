from django.shortcuts import render, redirect, get_object_or_404
from .models import Article, Category, Favorite, Tip, ArticleView
from .forms import ArticleForm, RegisterForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Count
import datetime
import json


def home(request):
    articles = Article.objects.all().order_by('-created_at')
    return render(request, 'blog/home.html', {'articles': articles})


def article_detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    session_key = request.session.session_key or request.session.save()
    if not ArticleView.objects.filter(article=article, session_key=session_key).exists():
        ArticleView.objects.create(article=article, session_key=session_key)
        article.views += 1
        article.save()
    return render(request, 'blog/article_detail.html', {'article': article})


@login_required
def add_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            a = form.save(commit=False)
            a.author = request.user
            a.save()
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


def stats_view(request, pk):
    article = get_object_or_404(Article, pk=pk)
    today = datetime.date.today()
    views = ArticleView.objects.filter(article=article).extra({'date': "date(timestamp)"}).values('date').annotate(
        count=Count('id'))
    data = {
        'dates': [str(v['date']) for v in views],
        'views': [v['count'] for v in views]
    }
    return JsonResponse(data)


def article_detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    article.views += 1
    article.save()


    chart_labels = ["Пн", "Вт", "Ср", "Чт", "Пт"]
    chart_data = [5, 3, 8, 6, 7]

    return render(request, 'blog/article_detail.html', {
        'article': article,
        'chart_labels': json.dumps(chart_labels),
        'chart_data': json.dumps(chart_data),
    })
