from unittest.mock import patch

from django.test import override_settings

from habits.tasks import send_telegram_message


@override_settings(TELEGRAM_TOKEN="test-token")
@patch("habits.tasks.requests.post")
def test_send_telegram_message(mock_post):
    send_telegram_message("123456", "Привет!")
    mock_post.assert_called_once()
    args, kwargs = mock_post.call_args
    assert kwargs["data"]["chat_id"] == "123456"
    assert "Привет!" in kwargs["data"]["text"]


from datetime import date, time
from unittest.mock import patch

import pytest

from accounts.models import CustomUser
from habits.models import Habit
from habits.tasks import send_reminder


@pytest.mark.django_db
@patch("habits.tasks.send_telegram_message")
def test_send_reminder(mock_send):
    user = CustomUser.objects.create(username="testuser")
    habit = Habit.objects.create(
        user=user,
        place="дом",
        time=time(8, 0),
        action="пить воду",
        duration=60,
        periodicity="daily",
        date=date.today(),
        chat_id="123456",
    )

    result = send_reminder(habit.id)
    mock_send.assert_called_once_with("123456", "🔔 Напоминание: пить воду в 08:00")
    assert result == f"Reminder OK for habit {habit.id}"
