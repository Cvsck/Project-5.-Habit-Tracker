from datetime import timedelta

from django.utils import timezone
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Habit
from .serializers import HabitSerializer
from .tasks import send_reminder


class HabitViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления привычками текущего пользователя.
    Поддерживает CRUD-операции и запускает отложенное напоминание при создании.
    """

    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Возвращает привычки текущего пользователя, отсортированные по id
        return Habit.objects.filter(user=self.request.user).order_by("id")

    def perform_create(self, serializer):
        # Сохраняем привычку с привязкой к текущему пользователю
        habit = serializer.save(user=self.request.user)

        # Запускаем отложенное напоминание через 10 секунд
        eta = timezone.now() + timedelta(seconds=10)
        send_reminder.apply_async((habit.id,), eta=eta)
