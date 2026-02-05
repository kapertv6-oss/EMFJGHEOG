import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = "7872623247:AAEth4pJELZdmyQfcYUf8c3Kzdo77uaAoYw"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# очки игрока
scores = {}

def keyboard(light_on: bool):
    if light_on:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="💡 Тушить свет", callback_data="off")]
            ]
        )
    else:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="🌑 Включить свет", callback_data="on")]
            ]
        )

@dp.message(Command("start"))
async def start(message: types.Message):
    scores[message.from_user.id] = 0
    await message.answer(
        "🎮 *Outlight*\n\n"
        "💡 Потуши свет — получи *1 очко*\n"
        "📊 Очки считаются автоматически",
        reply_markup=keyboard(True),
        parse_mode="Markdown"
    )

@dp.callback_query(lambda c: c.data in ["on", "off"])
async def play(callback: types.CallbackQuery):
    user_id = callback.from_user.id

    if user_id not in scores:
        scores[user_id] = 0

    if callback.data == "off":
        scores[user_id] += 1  # +1 очко за потушенный свет
        text = (
            "🌑 *Свет потушен!*\n"
            f"🏆 Очки: *{scores[user_id]}*"
        )
        kb = keyboard(False)
    else:
        text = (
            "💡 *Свет включён*\n"
            f"🏆 Очки: *{scores[user_id]}*"
        )
        kb = keyboard(True)

    await callback.message.edit_text(
        text,
        reply_markup=kb,
        parse_mode="Markdown"
    )
    await callback.answer()

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
