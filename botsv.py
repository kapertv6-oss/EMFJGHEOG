import asyncio
import random
import time
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = "7872623247:AAEth4pJELZdmyQfcYUf8c3Kzdo77uaAoYw"

bot = Bot(token=TOKEN)
dp = Dispatcher()

SIZE = 3
GAMES = {}

def new_field():
    return [[random.choice([0, 1]) for _ in range(SIZE)] for _ in range(SIZE)]

def toggle(field, x, y):
    for dx, dy in [(0,0), (1,0), (-1,0), (0,1), (0,-1)]:
        nx, ny = x + dx, y + dy
        if 0 <= nx < SIZE and 0 <= ny < SIZE:
            field[nx][ny] ^= 1

def is_win(field):
    return all(cell == 0 for row in field for cell in row)

def keyboard(field):
    kb = []
    for i in range(SIZE):
        row = []
        for j in range(SIZE):
            emoji = "🌕" if field[i][j] else "🌑"
            row.append(
                InlineKeyboardButton(
                    text=emoji,
                    callback_data=f"cell_{i}_{j}"
                )
            )
        kb.append(row)
    return InlineKeyboardMarkup(inline_keyboard=kb)

def game_text(user, moves, start_time):
    elapsed = int(time.time() - start_time)
    return (
        f"💡 *{user}, игра Lights Out*\n"
        f"Для победы нужно отключить весь свет!\n\n"
        f"Нажатие переключает кнопку и соседние.\n\n"
        f"⭐ Сложность: ⭐⭐\n"
        f"Нажатий: *{moves}*\n"
        f"⏱ Время: *{elapsed} сек*"
    )

@dp.message(Command("start"))
async def start(message: types.Message):
    field = new_field()
    GAMES[message.from_user.id] = {
        "field": field,
        "moves": 0,
        "time": time.time()
    }

    await message.answer(
        game_text(message.from_user.first_name, 0, GAMES[message.from_user.id]["time"]),
        reply_markup=keyboard(field),
        parse_mode="Markdown"
    )

@dp.callback_query(lambda c: c.data.startswith("cell_"))
async def click(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    if user_id not in GAMES:
        await callback.answer("Игра не найдена")
        return

    _, x, y = callback.data.split("_")
    x, y = int(x), int(y)

    game = GAMES[user_id]
    toggle(game["field"], x, y)
    game["moves"] += 1

    if is_win(game["field"]):
        elapsed = int(time.time() - game["time"])
        await callback.message.edit_text(
            f"🎉 *ПОБЕДА!*\n\n"
            f"Нажатий: *{game['moves']}*\n"
            f"⏱ Время: *{elapsed} сек*",
            parse_mode="Markdown"
        )
        GAMES.pop(user_id)
        await callback.answer()
        return

    await callback.message.edit_text(
        game_text(
            callback.from_user.first_name,
            game["moves"],
            game["time"]
        ),
        reply_markup=keyboard(game["field"]),
        parse_mode="Markdown"
    )
    await callback.answer()

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
