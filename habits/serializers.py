from rest_framework import serializers

from .models import Habit


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = "__all__"
        read_only_fields = ["user"]

    def validate(self, data):
        user = self.context["request"].user
        linked = data.get("linked_habit")
        reward = data.get("reward")
        is_pleasant = data.get("is_pleasant")
        duration = data.get("duration")
        periodicity = data.get("periodicity")

        # ❌ Нельзя одновременно указать linked_habit и reward
        if linked and reward:
            raise serializers.ValidationError(
                "Нельзя одновременно указать связанную привычку и вознаграждение."
            )

        # ⏱️ Время выполнения не должно превышать 120 секунд
        if duration and duration > 120:
            raise serializers.ValidationError(
                "Время выполнения не должно превышать 120 секунд."
            )

        # 🔗 Связанная привычка должна быть приятной
        if linked and not linked.is_pleasant:
            raise serializers.ValidationError(
                "Связанная привычка должна быть приятной."
            )

        # 🎁 Приятная привычка не может иметь награду или связанную привычку
        if is_pleasant and (reward or linked):
            raise serializers.ValidationError(
                "Приятная привычка не может иметь награду или связанную привычку."
            )

        # 🔐 Связанная привычка должна принадлежать текущему пользователю
        if linked and linked.user != user:
            raise serializers.ValidationError(
                "Связанная привычка должна принадлежать вам."
            )

        # 📅 Периодичность должна быть допустимой
        if periodicity not in ["daily", "weekly", "custom"]:
            raise serializers.ValidationError(
                "Недопустимое значение периодичности. Допустимы: daily, weekly, custom."
            )

        return data
