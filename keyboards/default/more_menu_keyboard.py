from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

more_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("Сравнение регионов России по проценту смертности")
        ],
        [
            KeyboardButton("На главную")
        ],
        [
            KeyboardButton("Скрыть")
        ]
    ],
    resize_keyboard=True
)
