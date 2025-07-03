from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from .models import PasswordResetCode, EmailVerificationCode, Profile
import random
from django.contrib.auth import authenticate, login
from .forms import EmailLoginForm, RegisterForm, EditProfileForm, ProfileAvatarForm
from django.template.loader import render_to_string
from django.db.models import Sum
from blog.models import Article




def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
            user = authenticate(request, username=user.username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Неверный email или пароль.')

        except User.DoesNotExist:
            messages.error(request, 'Пользователь с таким email не найден.')

    return render(request, 'registration/login.html')


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        users = User.objects.filter(email=email)

        if users.exists():
            user = users.first()  # берём первого пользователя
            code = str(random.randint(100000, 999999))
            PasswordResetCode.objects.create(user=user, code=code)

            html_message = render_to_string('auth/reset_code_email.html', {'code': code})
            plain_message = f'Ваш код: {code}'

            send_mail(
                subject='Код для сброса пароля',
                message=plain_message,
                from_email='noreply@devlog.com',
                recipient_list=[email],
                fail_silently=False,
                html_message=html_message
            )

            request.session['reset_user_id'] = user.id
            return redirect('verify_code')
        else:
            messages.error(request, 'Пользователь с таким email не найден.')
    return render(request, 'auth/forgot_password.html')


def verify_code(request):
    user_id = request.session.get('reset_user_id')
    if not user_id:
        return redirect('forgot_password')

    if request.method == 'POST':
        input_code = request.POST.get('code')
        code_obj = PasswordResetCode.objects.filter(user_id=user_id, code=input_code, is_used=False).first()

        if code_obj:
            code_obj.is_used = True
            code_obj.save()
            request.session['verified_for_reset'] = True
            return redirect('reset_password')
        else:
            messages.error(request, 'Неверный или использованный код.')
    return render(request, 'auth/verify_code.html')


def reset_password(request):
    user_id = request.session.get('reset_user_id')
    verified = request.session.get('verified_for_reset')

    if not user_id or not verified:
        return redirect('forgot_password')

    if request.method == 'POST':
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, 'Пароли не совпадают.')
        else:
            user = User.objects.get(id=user_id)
            user.set_password(password1)
            user.save()

            # Очистить сессию
            request.session.pop('reset_user_id')
            request.session.pop('verified_for_reset')

            # ✅ Автоматически авторизовать пользователя
            login(request, user)

            messages.success(request, 'Пароль успешно сброшен.')
            return redirect('profile')  # 🔁 Редирект в профиль (или на главную)

    return render(request, 'auth/reset_password.html')


@login_required
def send_verification_email(request):
    code = str(random.randint(100000, 999999))
    EmailVerificationCode.objects.create(user=request.user, code=code)

    send_mail(
        'Подтверждение email',
        f'Ваш код подтверждения: {code}',
        'noreply@devlog.com',
        [request.user.email],
        fail_silently=False
    )

    messages.success(request, 'Код отправлен на email.')
    return redirect('verify_email')


@login_required
def verify_email(request):
    if request.method == 'POST':
        code_input = request.POST.get('code')
        code_obj = EmailVerificationCode.objects.filter(
            user=request.user, code=code_input, is_used=False
        ).first()

        if code_obj:
            code_obj.is_used = True
            code_obj.save()
            request.user.profile.email_verified = True
            request.user.profile.save()
            messages.success(request, 'Email успешно подтверждён.')
            return redirect('profile')
        else:
            messages.error(request, 'Неверный код')

    return render(request, 'accounts/verify_email.html')


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.get_or_create(user=user)  # <-- безопасно, не создаст дубликат
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def edit_profile(request):
    user = request.user
    profile = user.profile

    if request.method == 'POST':
        user_form = EditProfileForm(request.POST, instance=user)
        avatar_form = ProfileAvatarForm(request.POST, request.FILES, instance=profile)
        if user_form.is_valid() and avatar_form.is_valid():
            user = user_form.save()
            if user_form.cleaned_data['password']:
                user.set_password(user_form.cleaned_data['password'])
                user.save()
            avatar_form.save()
            login(request, user)  # Перелогиниваем, если пароль изменился

            messages.success(request, "Обновление профиля успешно завершено!")

            return redirect('profile')
        else:
            messages.error(request, "Пожалуйста, исправьте ошибки в форме.")
    else:
        user_form = EditProfileForm(instance=user)
        avatar_form = ProfileAvatarForm(instance=profile)

    return render(request, 'profile/edit_profile.html', {
        'user_form': user_form,
        'avatar_form': avatar_form
    })


@login_required
def profile_view(request):
    user = request.user
    articles = Article.objects.filter(author=user)
    total_views = articles.aggregate(Sum('views'))['views__sum'] or 0

    # данные для графика
    chart_labels = [article.title for article in articles]
    chart_data = [article.views for article in articles]

    context = {
        'articles': articles,
        'profile': user.profile,
        'total_views': total_views,
        'chart_labels': chart_labels,
        'chart_data': chart_data,
    }
    return render(request, 'profile/profile.html', context)