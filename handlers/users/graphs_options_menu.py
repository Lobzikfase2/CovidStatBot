from aiogram import types

from keyboards.default import interval_options, graphs_options, stats_type_options, options_menu
from keyboards.inline import get_started_markup
from loader import dp, db


@dp.message_handler(text="Интервал показа статистики")
async def show_interval_options(message: types.Message):
    """
    Присылает пользователю меню настроек интервала показа статистики на графике
    """
    await message.answer("<i>интервал показа статистики</i>", reply_markup=interval_options, disable_notification=True)


@dp.message_handler(text="За последний месяц")
async def set_month(message: types.Message):
    """
    Действия бота, при нажатии кнопки "За последний месяц"
    """
    db.update_user_interval(message.from_user.id, 1)
    await message.answer("<b>Теперь на графиках отображается статистика за последний месяц</b>",
                         reply_markup=graphs_options)


@dp.message_handler(text="За последний год")
async def set_year(message: types.Message):
    """
    Действия бота, при нажатии кнопки "За последний год"
    """
    db.update_user_interval(message.from_user.id, 2)
    await message.answer("<b>Теперь на графиках отображается статистика за последний год</b>",
                         reply_markup=graphs_options)

@dp.message_handler(text="За всё время")
async def set_all_time(message: types.Message):
    """
    Действия бота, при нажатии кнопки "За всё время"
    """
    db.update_user_interval(message.from_user.id, 3)
    await message.answer("<b>Теперь на графиках отображается статистика за всё время</b>", reply_markup=graphs_options)


@dp.message_handler(text="Тип статистических данных")
async def show_graphs_type_options(message: types.Message):
    """
    Присылает пользователю меню настроек типа статистических данных,
    отображаемых на графике
    """
    await message.answer("<i>тип статистических данных</i>", reply_markup=stats_type_options, disable_notification=True)


@dp.message_handler(text="Отображать на графике прирост случаев за день")
async def set_type_one(message: types.Message):
    """
    Действия бота, при нажатии кнопки "Отображать на графике прирост случаев за день"
    """
    db.update_user_stats_type(message.from_user.id, 1)
    await message.answer("<b>Теперь на графиках отображается прирост случаев за день</b>", reply_markup=graphs_options)

@dp.message_handler(text="Отображать на графике общее число случаев")
async def set_type_two(message: types.Message):
    """
    Действия бота, при нажатии кнопки "Отображать на графике общее число случаев"
    """
    db.update_user_stats_type(message.from_user.id, 2)
    await message.answer("<b>Теперь на графиках отображается общее число случаев</b>", reply_markup=graphs_options)


@dp.message_handler(text="⏪ Назад ⏪")
async def go_back(message: types.Message):
    """
    Действия бота, при нажатии кнопки "⏪ Назад ⏪"
    """
    await message.answer("<-", parse_mode=types.ParseMode.MARKDOWN, reply_markup=graphs_options,
                         disable_notification=True)


@dp.message_handler(text="⏪⏪ Назад ⏪⏪")
async def go_on_the_first_page(message: types.Message):
    """
    Действия бота, при нажатии кнопки "⏪⏪ Назад ⏪⏪"
    """
    await message.answer("<--", parse_mode=types.ParseMode.MARKDOWN, reply_markup=options_menu,
                         disable_notification=True)
