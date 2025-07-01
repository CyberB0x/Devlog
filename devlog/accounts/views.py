from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from .models import PasswordResetCode
import random
from django.contrib.auth import authenticate, login
from .forms import EmailLoginForm
from django.template.loader import render_to_string


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

    return render(request, 'auth/login.html')


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
