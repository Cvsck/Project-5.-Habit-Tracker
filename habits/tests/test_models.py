import pytest
from django.core.exceptions import ValidationError

from accounts.models import CustomUser
from habits.models import Habit

pytestmark = pytest.mark.django_db


def test_valid_habit_creation():
    """
    Проверяет базовое создание привычки:
    - создаётся пользователь
    - создаётся привычка с минимально необходимыми полями
    - поле action сохраняется корректно
    """
    user = CustomUser.objects.create(username="testuser")
    habit = Habit.objects.create(
        user=user,
        place="дом",
        time="08:00",
        action="пить воду",
        duration=60,
        periodicity="daily",
    )
    assert habit.action == "пить воду"


def test_invalid_habit_with_reward_and_linked_habit():
    """
    Проверяет бизнес-валидацию:
    - нельзя одновременно указать награду и связанную привычку
    - ожидается ValidationError при вызове full_clean()
    """
    user = CustomUser.objects.create(username="testuser")
    pleasant = Habit.objects.create(
        user=user,
        place="дом",
        time="08:00",
        action="читать",
        duration=30,
        periodicity="daily",
        is_pleasant=True,
    )
    habit = Habit(
        user=user,
        place="дом",
        time="09:00",
        action="пить воду",
        duration=60,
        periodicity="daily",
        reward="чай",
        linked_habit=pleasant,
    )
    with pytest.raises(ValidationError):
        habit.full_clean()


def test_linked_habit_must_be_pleasant():
    """
    Проверяет, что связанная привычка должна быть приятной:
    - создаётся привычка с is_pleasant=False
    - при указании её как linked_habit возникает ValidationError
    """
    user = CustomUser.objects.create(username="testuser")
    unpleasant = Habit.objects.create(
        user=user,
        place="дом",
        time="08:00",
        action="уборка",
        duration=30,
        periodicity="daily",
        is_pleasant=False,
    )
    habit = Habit(
        user=user,
        place="дом",
        time="09:00",
        action="пить воду",
        duration=60,
        periodicity="daily",
        linked_habit=unpleasant,
    )
    with pytest.raises(ValidationError):
        habit.full_clean()


def test_habit_str_representation():
    """
    Проверяет метод __str__ модели Habit:
    - строка должна содержать действие, время и пометку приятности
    - используется формат: 'действие в HH:MM (приятная/вредная)'
    """
    user = CustomUser.objects.create(username="testuser")
    habit = Habit.objects.create(
        user=user,
        place="дом",
        time="08:00",
        action="пить воду",
        duration=60,
        periodicity="daily",
        is_pleasant=True,
    )
    assert str(habit) == "пить воду в 08:00 (приятная)"
