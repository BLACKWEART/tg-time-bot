import os
import asyncio
from datetime import datetime, timezone
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# 🔐 ТОКЕН БЕРЁТСЯ ИЗ ENV (Render / GitHub)
TOKEN = os.getenv("TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()

# ⏱ РЕАЛЬНЫЙ старт отсчёта (фиксируется при запуске)
REAL_START_TIME = datetime.now(timezone.utc)

# 📅 ВИРТУАЛЬНОЕ НАЧАЛО
VIRTUAL_START_YEAR = 2015


def get_virtual_date():
    now = datetime.now(timezone.utc)
    delta = now - REAL_START_TIME

    total_minutes = delta.total_seconds() / 60

    # 1 реальный день = 1 виртуальный год
    years_passed = int(total_minutes // 1440)
    year = VIRTUAL_START_YEAR + years_passed

    remaining_minutes = total_minutes % 1440

    # 1 месяц = 2 часа = 120 минут
    month = int(remaining_minutes // 120) + 1
    remaining_minutes %= 120

    # 1 день = 4 минуты
    day = int(remaining_minutes // 4) + 1

    # ограничения
    if month > 12:
        month = 12
    if day > 30:
        day = 30

    return f"{day:02d}.{month:02d}.{year:04d}"


def get_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="⏳ Проверить время", callback_data="check_time")]
        ]
    )


@dp.message(CommandStart())
async def start(message: types.Message):
    await message.answer(
        "🕰 Виртуальное время\n"
        "Начало: 01.01.2015\n"
        "Скорость: 1 день = 1 год\n\n"
        "Нажми кнопку ⬇️",
        reply_markup=get_keyboard()
    )


@dp.callback_query(lambda c: c.data == "check_time")
async def check_time(callback: types.CallbackQuery):
    date = get_virtual_date()
    await callback.message.answer(
        f"📅 {date}",
        reply_markup=get_keyboard()
    )
    await callback.answer()


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
