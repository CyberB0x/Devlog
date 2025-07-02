import os.path

from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Count, Sum
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.db.models.functions import TruncDate
from .utils import render_editorjs_to_html
from django.db.models import Q

import datetime
import json

from .models import Article, Category, Favorite, Tip, ArticleView, Like
from .forms import ArticleForm, CommentForm


def home(request):
    articles = Article.objects.all().order_by('-created_at')
    return render(request, 'blog/home.html', {'articles': articles})


def article_detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    comments = article.comments.all().order_by('-created_at')

    # Просмотр: по session_key
    session_key = request.session.session_key
    if not session_key:
        request.session.create()
        session_key = request.session.session_key

    if not ArticleView.objects.filter(article=article, session_key=session_key).exists():
        ArticleView.objects.create(article=article, session_key=session_key)
        article.views += 1
        article.save()

    # Комментарии
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

    is_liked = False
    if request.user.is_authenticated:
        is_liked = article.like_set.filter(user=request.user).exists()

    return render(request, 'blog/article_detail.html', {
        'article': article,
        'comments': comments,
        'form': form,
        'is_liked': is_liked,
        'like_count': article.like_set.count(),
    })


@login_required
def add_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user

            # Преобразуем Editor.js JSON → HTML
            raw_content = request.POST.get("content_html", "")
            article.content_html = render_editorjs_to_html(raw_content)

            article.save()
            return redirect('article_detail', pk=article.pk)
    else:
        form = ArticleForm()
    return render(request, 'blog/article_form.html', {'form': form})

@login_required
def delete_article(request, pk):
    article = get_object_or_404(Article, pk=pk, author=request.user)
    article.delete()
    return redirect('home')



# 📊 Данные для графика просмотров (json)
def stats_view(request, pk):
    views = (
        ArticleView.objects
        .filter(article__author_id=pk)
        .annotate(date=TruncDate('timestamp'))
        .values('date')
        .annotate(count=Count('id'))
        .order_by('date')
    )

    data = {
        'dates': [str(v['date']) for v in views],
        'views': [v['count'] for v in views]
    }
    return JsonResponse(data)


@csrf_exempt
@login_required
def toggle_like(request, pk):
    if request.method == "POST":
        article = get_object_or_404(Article, pk=pk)
        like, created = Like.objects.get_or_create(article=article, user=request.user)

        if not created:
            like.delete()
            liked = False
        else:
            liked = True

        return JsonResponse({
            'liked': liked,
            'like_count': article.like_set.count()
        })


@csrf_exempt
def upload_image(request):
    if request.method == 'POST':
        image = request.FILES.get('image') or request.FILES.get('file')
        if not image:
            return JsonResponse({"success": 0, "message": "No file uploaded"}, status=400)

        # Сохраняем в MEDIA_ROOT/articles/
        path = default_storage.save(f'articles/{image.name}', ContentFile(image.read()))
        image_url = os.path.join(settings.MEDIA_URL, path)

        return JsonResponse({
            "success": 1,
            "file": {
                "url": image_url
            }
        })

    return JsonResponse({"success": 0, "message": "Invalid request"}, status=400)





def search_articles(request):
    query = request.GET.get('q', '')
    results = Article.objects.filter(
        Q(title__icontains=query) |
        Q(content_html__icontains=query)
    ).order_by('-created_at') if query else []

    return render(request, 'blog/search_results.html', {
        'query': query,
        'results': results,
    })