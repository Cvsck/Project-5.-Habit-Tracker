import requests
from django.conf import settings


def send_telegram_message(chat_id: str, text: str):
    """
    Отправляет сообщение в Telegram через Bot API.
    """
    token = settings.TELEGRAM_BOT_TOKEN

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
