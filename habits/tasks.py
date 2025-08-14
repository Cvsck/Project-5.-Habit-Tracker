from datetime import date

from celery import shared_task

from telegram_bot.utils import send_telegram_message

from .models import Habit


@shared_task
def send_reminder(habit_id=None):
    habit = Habit.objects.filter(id=habit_id).first()
    if not habit:
        print(f"⚠️ Habit {habit_id} not found")
        return

    message = f"🔔 Напоминание: {habit.action} в {habit.time.strftime('%H:%M')}"
    print(f"📨 Sending reminder for habit {habit_id}: {message}")

    # ✅ Используем telegram_chat_id владельца привычки
    if habit.user.telegram_chat_id:
        send_telegram_message(habit.user.telegram_chat_id, message)
    else:
        print(f"⚠️ No telegram_chat_id for user {habit.user.username}")

    return f"Reminder OK for habit {habit_id}"


@shared_task
def send_daily_reminders():
    now = date.today()
    print(f"⏰ Checking habits for date {now}")

    habits = Habit.objects.filter(date=now)
    print(f"📌 Found {habits.count()} habits")

    for habit in habits:
        send_reminder.delay(habit.id)
