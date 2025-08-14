# Project-5.-Habit-Tracker
git clone https://github.com/your-username/Project-5.-Habit-Tracker.git
cd Project-5.-Habit-Tracker
python -m venv .venv
source .venv/bin/activate  # или .venv\Scripts\activate на Windows
pip install -r requirements.txt
pytest --cov=habits --cov-report=html
Документация
Автоматически генерируется через DRF. Эндпоинты:

POST /auth/register/ — регистрация

POST /auth/login/ — авторизация

GET /api/habits/ — список привычек

GET /api/public-habits/ — публичные привычки

POST /api/habits/ — создать привычку

PUT /api/habits/{id}/ — редактировать

DELETE /api/habits/{id}/ — удалить