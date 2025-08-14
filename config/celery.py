import os

from celery import Celery

# Установка переменной окружения для Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

# Создание экземпляра Celery
app = Celery("habit_tracker")

# Загрузка конфигурации из Django settings
app.config_from_object("django.conf:settings", namespace="CELERY")

# Автоматическое обнаружение задач в tasks.py
app.autodiscover_tasks()
