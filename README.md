# 🔐 Django Password Reset Flow with Email Verification

This project provides a complete, secure, and user-friendly password reset workflow using one-time verification codes sent via email. It's ideal for blogs, SaaS apps, or any Django-based site that handles user accounts.

## 🚀 Features

- Request password reset by email
- Generate and send a 6-digit email code
- Verify the email code
- Reset password securely with validation
- Auto-login after successful reset
- User-friendly messages and form validation

## 🛠 Tech Stack

- Python 3.12+
- Django 5.x
- SQLite / MySQL
- Bootstrap 5 (optional styling)
- Django Forms, Messages, and Sessions

## 📦 Installation

```bash
    git clone https://github.com/your-username/django-password-reset.git
    cd django-password-reset
    python -m venv venv
    source venv/bin/activate  # or venv\Scripts\activate on Windows
    pip install -r requirements.txt
    python manage.py migrate
    python manage.py runserver
```

# 📁 Project Structure
```commandline
   accounts/
├── models.py       # PasswordResetCode model
├── views.py        # Forgot → Verify → Reset logic
├── forms.py        # Email, Code, and Password forms
├── templates/auth/
│   ├── forgot_password.html
│   ├── verify_code.html
│   └── reset_password.html

```

# 👤 Author
* Arslonbek Erkinov
* 🔗 LinkedIn Profile https://www.linkedin.com/in/arslon-erkinov-6723aa1a2/

