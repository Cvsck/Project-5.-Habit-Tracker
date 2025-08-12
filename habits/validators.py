from rest_framework.exceptions import ValidationError


def validate_reward_or_linked_habit(data):
    reward = data.get("reward")
    linked_habit = data.get("linked_habit")
    if reward and linked_habit:
        raise ValidationError(
            "Нельзя одновременно указать вознаграждение и связанную привычку."
        )


def validate_duration(data):
    duration = data.get("duration")
    if duration and duration > 120:
        raise ValidationError(
            "Время выполнения привычки не должно превышать 120 секунд."
        )


def validate_linked_habit_is_pleasant(data):
    linked_habit = data.get("linked_habit")
    if linked_habit and not linked_habit.is_pleasant:
        raise ValidationError("Связанная привычка должна быть приятной.")


def validate_pleasant_has_no_reward_or_link(data):
    is_pleasant = data.get("is_pleasant")
    reward = data.get("reward")
    linked_habit = data.get("linked_habit")
    if is_pleasant and (reward or linked_habit):
        raise ValidationError(
            "Приятная привычка не может иметь вознаграждение или связанную привычку."
        )


def validate_periodicity(data):
    periodicity = data.get("periodicity")
    if periodicity not in ["daily", "weekly"]:
        raise ValidationError("Периодичность должна быть 'daily' или 'weekly'.")
