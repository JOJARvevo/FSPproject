# School Event Landing (FastAPI + Jinja2)

Одностраничный лендинг для школьного мероприятия (пример — День науки). Реализованы блоки с датой/местом, описанием, программой, формой регистрации, контактами, таймером обратного отсчета и переключением светлой/тёмной темы. Заявки сохраняются в SQLite. Есть Telegram-бот для выгрузки заявок в Excel.

## Быстрый старт
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```
Приложение будет доступно на `http://127.0.0.1:8000/`.

## Переменные окружения для бота
- `TELEGRAM_BOT_TOKEN` — токен бота.
- `TELEGRAM_ALLOWED_CHAT_IDS` — список разрешённых chat_id через запятую (если пусто, доступ открыт всем).

## Запуск Telegram-бота
```bash
TELEGRAM_BOT_TOKEN=... TELEGRAM_ALLOWED_CHAT_IDS=123,456 python telegram_bot.py
```
Команды: `/start`, `/count` (кол-во заявок), `/export` (Excel с заявками).
