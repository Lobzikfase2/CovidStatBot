from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

options_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Настройки отображения графиков")
        ],
        [
            KeyboardButton("Изменить регион")
        ],
        [
            KeyboardButton(text="Скрыть")
        ]
    ],
    resize_keyboard=True
)
