from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

interval_options = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("За последний месяц")
        ],
        [
            KeyboardButton(text="За последний год")
        ],
        [
            KeyboardButton(text="За всё время")
        ],
        [
            KeyboardButton(text="⏪ Назад ⏪")
        ],
        [
            KeyboardButton(text="Скрыть")
        ]
    ],
    resize_keyboard=True
)
