from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

stats_type_options = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Отображать на графике прирост случаев за день")
        ],
        [
            KeyboardButton("Отображать на графике общее число случаев")
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
