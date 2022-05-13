from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

stats_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("Мировая статистика")
        ],
        [
            KeyboardButton(text="Всероссийская статистика")
        ],
        [
            KeyboardButton(text="Региональная статистика")
        ],
        [
            KeyboardButton(text="Ещё")
        ],
        [
            KeyboardButton(text="Скрыть")
        ]
    ],
    resize_keyboard=True
)
