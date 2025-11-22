import asyncio
import os
from datetime import datetime
from pathlib import Path

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import FSInputFile
from openpyxl import Workbook
from sqlalchemy.orm import Session

from app.database import Registration, SessionLocal, create_db

create_db()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
ALLOWED_CHATS = {
    chat_id.strip()
    for chat_id in os.getenv("TELEGRAM_ALLOWED_CHAT_IDS", "").split(",")
    if chat_id.strip()
}

dispatcher = Dispatcher()


def export_registrations(path: Path) -> Path:
    wb = Workbook()
    ws = wb.active
    ws.title = "Заявки"
    ws.append(
        ["ID", "ФИО", "Email", "Телефон", "Класс/роль", "Комментарий", "Создано"]
    )
    with SessionLocal() as db:  # type: Session
        for row in db.query(Registration).order_by(Registration.created_at).all():
            ws.append(
                [
                    row.id,
                    row.full_name,
                    row.email,
                    row.phone,
                    row.grade,
                    row.comment or "",
                    row.created_at.strftime("%Y-%m-%d %H:%M"),
                ]
            )
    wb.save(path)
    return path


async def send_usage(message: types.Message) -> None:
    await message.answer(
        "Команды:\n"
        "/export — выгрузить заявки в Excel\n"
        "/count — показать количество заявок"
    )


def is_allowed(user_id: int) -> bool:
    return not ALLOWED_CHATS or str(user_id) in ALLOWED_CHATS


@dispatcher.message(Command("start"))
async def start(message: types.Message) -> None:
    if not is_allowed(message.from_user.id):
        await message.answer("Доступ ограничен.")
        return
    await send_usage(message)


@dispatcher.message(Command("count"))
async def count(message: types.Message) -> None:
    if not is_allowed(message.from_user.id):
        await message.answer("Доступ ограничен.")
        return
    with SessionLocal() as db:
        total = db.query(Registration).count()
    await message.answer(f"Всего заявок: {total}")


@dispatcher.message(Command("export"))
async def export(message: types.Message) -> None:
    if not is_allowed(message.from_user.id):
        await message.answer("Доступ ограничен.")
        return
    await message.answer("Готовим файл...")
    export_path = Path("registrations_export.xlsx")
    export_registrations(export_path)
    await message.answer_document(FSInputFile(export_path))
    export_path.unlink(missing_ok=True)


async def main() -> None:
    if not BOT_TOKEN:
        raise RuntimeError("TELEGRAM_BOT_TOKEN не задан")
    bot = Bot(token=BOT_TOKEN)
    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Bot stopped.")
