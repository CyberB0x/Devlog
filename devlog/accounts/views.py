from django.contrib import messages
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import render, redirect
import random
from .models import PasswordResetCode
from .forms import EmailForm, CodeVerificationForm, PasswordResetForm

def forgot_password(request):
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
                code = str(random.randint(100000, 999999))
                PasswordResetCode.objects.create(user=user, code=code)

                send_mail(
                    'Код сброса пароля',
                    f'Ваш код: {code}',
                    'noreply@devlog.com',
                    [email],
                    fail_silently=False
                )

                request.session['reset_user_id'] = user.id
                return redirect('verify_code')
            except User.DoesNotExist:
                messages.error(request, 'Email не найден.')
    else:
        form = EmailForm()
    return render(request, 'auth/forgot_password.html', {'form': form})

def verify_code(request):
    user_id = request.session.get('reset_user_id')
    if not user_id:
        return redirect('forgot_password')

    if request.method == 'POST':
        form = CodeVerificationForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            code_obj = PasswordResetCode.objects.filter(user_id=user_id, code=code, is_used=False).first()
            if code_obj:
                code_obj.is_used = True
                code_obj.save()
                request.session['verified'] = True
                return redirect('reset_password')
            else:
                messages.error(request, 'Неверный код.')
    else:
        form = CodeVerificationForm()
    return render(request, 'auth/verify_code.html', {'form': form})

def reset_password(request):
    user_id = request.session.get('reset_user_id')
    verified = request.session.get('verified')

    if not (user_id and verified):
        return redirect('forgot_password')

    user = User.objects.get(id=user_id)

    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            user.set_password(form.cleaned_data['new_password'])
            user.save()
            messages.success(request, 'Пароль успешно сброшен.')
            return redirect('login')
    else:
        form = PasswordResetForm()

    return render(request, 'auth/reset_password.html', {'form': form})
