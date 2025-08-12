from datetime import date

import requests
from celery import shared_task
from django.conf import settings

from .models import Habit


def send_telegram_message(chat_id: str, text: str):
    """
    Отправляет сообщение в Telegram через Bot API.
    """
    token = settings.TELEGRAM_TOKEN  # Убедись, что он есть в settings.py
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
    }
    try:
        response = requests.post(url, data=payload)
        response.raise_for_status()
        print(f"✅ Telegram sent to {chat_id}")
    except requests.RequestException as e:
        print(f"❌ Telegram error: {e}")


@shared_task
def send_reminder(habit_id=None):
    habit = Habit.objects.filter(id=habit_id).first()
    if not habit:
        print(f"⚠️ Habit {habit_id} not found")
        return

    message = f"🔔 Напоминание: {habit.action} в {habit.time.strftime('%H:%M')}"
    print(f"📨 Sending reminder for habit {habit_id}: {message}")

    if habit.chat_id:
        send_telegram_message(habit.chat_id, message)

    return f"Reminder OK for habit {habit_id}"


@shared_task
def send_daily_reminders():
    now = date.today()
    print(f"⏰ Checking habits for date {now}")

    habits = Habit.objects.filter(date=now)
    print(f"📌 Found {habits.count()} habits")

    for habit in habits:
        send_reminder.delay(habit.id)
