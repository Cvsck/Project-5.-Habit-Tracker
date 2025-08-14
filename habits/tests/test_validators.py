import pytest
from django.core.exceptions import ValidationError
from rest_framework.test import APIRequestFactory

from accounts.models import CustomUser
from habits.models import Habit
from habits.serializers import HabitSerializer


@pytest.mark.django_db
def test_validate_linked_habit_is_pleasant_error():
    user = CustomUser.objects.create(username="testuser")
    linked = Habit.objects.create(
        user=user,
        place="дом",
        time="08:00",
        action="уборка",
        duration=30,
        periodicity="daily",
        is_pleasant=False,
    )

    data = {
        "place": "дом",
        "time": "09:00",
        "action": "пить воду",
        "duration": 60,
        "periodicity": "daily",
        "linked_habit": linked.id,  # ✅ передаём ID
    }

    factory = APIRequestFactory()
    request = factory.post("/fake-url/")
    request.user = user

    serializer = HabitSerializer(data=data, context={"request": request})
    assert not serializer.is_valid()
    assert "Связанная привычка должна быть приятной" in str(serializer.errors)


@pytest.mark.django_db
def test_serializer_invalid_duration():
    user = CustomUser.objects.create(username="testuser")
    factory = APIRequestFactory()
    request = factory.post("/fake-url/")
    request.user = user

    data = {
        "place": "дом",
        "time": "08:00",
        "action": "медитация",
        "duration": 150,  # ❌ превышает лимит
        "periodicity": "daily",
        "is_pleasant": True,
    }

    serializer = HabitSerializer(data=data, context={"request": request})
    assert not serializer.is_valid()
    assert "Время выполнения не должно превышать 120 секунд." in str(serializer.errors)
