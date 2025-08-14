from datetime import date, time

import pytest
from rest_framework.test import APIClient

from accounts.models import CustomUser
from habits.models import Habit


@pytest.mark.django_db
def test_get_habit_list():
    user = CustomUser.objects.create_user(username="testuser", email="test@example.com", password="pass")

    Habit.objects.create(
        user=user,
        place="дом",
        time=time(8, 0),
        action="пить воду",
        duration=60,
        periodicity="daily",
        date=date.today(),
    )

    client = APIClient()
    client.force_authenticate(user=user)
    response = client.get("/api/habits/")

    assert response.status_code == 200
    assert response.data["count"] == 1
    assert len(response.data["results"]) == 1
    assert response.data["results"][0]["action"] == "пить воду"
