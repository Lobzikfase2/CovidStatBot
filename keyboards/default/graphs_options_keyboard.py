from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

graphs_options = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("Интервал показа статистики")
        ],
        [
            KeyboardButton(text="Тип статистических данных")
        ],
        [
            KeyboardButton(text="⏪⏪ Назад ⏪⏪")
        ],
        [
            KeyboardButton(text="Скрыть")
        ]
    ],
    resize_keyboard=True
)
