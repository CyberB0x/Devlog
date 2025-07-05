# 🧠 DevLog — Developer Blog Platform (Django + Bootstrap)

DevLog is a modern blogging platform built with Django. It allows developers to share articles, track views, upload images, and manage profiles with avatars. The system includes secure authentication, email verification, password reset via code, and view statistics per article and per user.


## 🚀 Features

- 📝 Create and manage articles with Markdown
- 📊 Article view counters and statistics (chart per user)
- 🧑‍💻 Profile page with avatar, bio, and total views
- 🔐 Email/password authentication
- ✅ Email verification and password reset via 6-digit code
- 🖼 Upload images with preview
- ❤️ Like system per article
- 🔍 Search and filter articles by title
- 📬 Contact and social links (optional)
- 🌓 Dark/light Bootstrap theme support

## 🔧 Tech Stack

- Python 3.12+
- Django 5.x
- Bootstrap 5
- Chart.js for statistics
- SQLite/MySQL support
- Gmail or SMTP backend for email

## 🛠 Installation

```bash
    git clone https://github.com/yourusername/devlog.git
    cd devlog
    python -m venv venv
    source venv/bin/activate  # or venv\Scripts\activate on Windows
    pip install -r requirements.txt
    python manage.py migrate
    python manage.py runserver
```

# Create Superuser
``` bash
    python manage.py createsuperuser
```

# 📧 Email Setup
*In settings.py, set:
```commandline
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    EMAIL_HOST_USER = 'your_email@gmail.com'
    EMAIL_HOST_PASSWORD = 'your_app_password'

```

# 🧪 Tests
* Coming soon…

# 🤝 Contributing
* Pull requests are welcome. For major changes, please open an issue first.

# 🏁 Project Status
* ✅ MVP done — currently used as a personal portfolio project.
* 📈 Planned: comments, tags, categories, subscriptions.

# 🙌 Support This Project
If you find DevLog helpful or inspiring, consider supporting the project!
Your support helps me maintain, improve and expand this open-source platform.
* ☕ Buy Me a Coffee https://www.donationalerts.com/r/cyberb0x
* 📬 Or just share it with fellow developers and give it a ⭐️ on GitHub!
* Thank you for your support! ❤️