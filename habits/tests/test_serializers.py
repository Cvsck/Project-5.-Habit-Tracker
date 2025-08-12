import pytest
from rest_framework.test import APIRequestFactory

from accounts.models import CustomUser
from habits.models import Habit
from habits.serializers import HabitSerializer


@pytest.mark.django_db
def test_serializer_valid_data():
    user = CustomUser.objects.create(username="testuser")
    factory = APIRequestFactory()
    request = factory.post("/fake-url/")
    request.user = user

    data = {
        "place": "дом",
        "time": "08:00",
        "action": "пить воду",
        "duration": 60,
        "periodicity": "daily",
        "is_pleasant": True,
    }

    serializer = HabitSerializer(data=data, context={"request": request})
    assert serializer.is_valid()

    # 🔧 Вставляем user вручную перед сохранением
    validated_data = serializer.validated_data
    validated_data["user"] = user
    habit = Habit.objects.create(**validated_data)

    assert habit.action == "пить воду"
    assert habit.user == user


@pytest.mark.django_db
def test_serializer_invalid_reward_and_linked():
    user = CustomUser.objects.create(username="testuser")
    factory = APIRequestFactory()
    request = factory.post("/fake-url/")
    request.user = user

    # Создаём linked_habit
    linked = Habit.objects.create(
        user=user,
        place="дом",
        time="08:00",
        action="читать",
        duration=30,
        periodicity="daily",
        is_pleasant=True,
    )

    # Пробуем создать привычку с reward и linked_habit одновременно
    data = {
        "place": "дом",
        "time": "09:00",
        "action": "пить воду",
        "duration": 60,
        "periodicity": "daily",
        "reward": "чай",
        "linked_habit": linked.id,
    }

    serializer = HabitSerializer(data=data, context={"request": request})
    assert not serializer.is_valid()
    assert "non_field_errors" in serializer.errors
