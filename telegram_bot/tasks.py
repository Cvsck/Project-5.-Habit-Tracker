# telegram_bot/tasks.py

import requests
from django.conf import settings


def send_telegram_message(chat_id, text):
    """
    Отправляет сообщение в Telegram-чат по chat_id.
    Использует токен из .env (TELEGRAM_BOT_TOKEN).
    """
    token = settings.TELEGRAM_BOT_TOKEN
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML",  # можно убрать, если не нужен формат
    }

    try:
        response = requests.post(url, data=payload, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        # Можно логировать ошибку или вернуть None
        print(f"❌ Ошибка при отправке Telegram-сообщения: {e}")
        return None
