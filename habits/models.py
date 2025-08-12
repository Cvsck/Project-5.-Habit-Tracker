# habits/models.py
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models

User = get_user_model()


class Habit(models.Model):
    PERIODICITY_CHOICES = [
        ("daily", "Ежедневно"),
        ("weekly", "Раз в неделю"),
        ("custom", "По графику"),
    ]

    action = models.CharField(max_length=100)
    place = models.CharField(max_length=100)
    time = models.TimeField()
    date = models.DateField(null=True, blank=True)
    is_pleasant = models.BooleanField(default=False)
    reward = models.CharField(max_length=100, blank=True, null=True)
    periodicity = models.CharField(max_length=20, choices=PERIODICITY_CHOICES)
    duration = models.PositiveIntegerField(
        help_text="Продолжительность в секундах"
    )  # seconds
    is_public = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="habits")
    linked_habit = models.ForeignKey(
        "self", on_delete=models.SET_NULL, null=True, blank=True
    )
    chat_id = models.CharField(max_length=64, blank=True, null=True)

    def clean(self):
        # ❌ Нельзя одновременно указать linked_habit и reward
        if self.linked_habit and self.reward:
            raise ValidationError(
                "Нельзя одновременно указать связанную привычку и вознаграждение."
            )

        # ⏱️ Время выполнения не должно превышать 120 секунд
        if self.duration > 120:
            raise ValidationError("Время выполнения не должно превышать 120 секунд.")

        # 🔗 Связанная привычка должна быть приятной
        if self.linked_habit and not self.linked_habit.is_pleasant:
            raise ValidationError("Связанная привычка должна быть приятной.")

        # 🎁 Приятная привычка не может иметь награду или связанную привычку
        if self.is_pleasant and (self.reward or self.linked_habit):
            raise ValidationError(
                "Приятная привычка не может иметь награду или связанную привычку."
            )

        # 📅 Периодичность не может быть больше 7 дней — если custom, нужно уточнять отдельно
        if self.periodicity == "custom":
            pass  # можно добавить логику позже
        elif self.periodicity == "weekly":
            pass  # допустимо
        elif self.periodicity == "daily":
            pass  # допустимо
        else:
            raise ValidationError("Недопустимое значение периодичности.")

    def __str__(self):
        return f"{self.action} в {self.time} ({'приятная' if self.is_pleasant else 'полезная'})"
