from aiogram import types

from keyboards.default import stats_menu, options_menu
from keyboards.inline.callback_datas import get_started_callback
from loader import dp


@dp.callback_query_handler(get_started_callback.filter(type="stats"))
async def show_menu(callback: types.CallbackQuery):
    """
    Действия бота, при нажатии кнопки "Статистика" в инлайн меню
    """
    await callback.message.answer(text="/stats", reply_markup=stats_menu, disable_notification=True)
    await callback.answer()


@dp.callback_query_handler(get_started_callback.filter(type="options"))
async def show_menu(callback: types.CallbackQuery):
    """
    Действия бота, при нажатии кнопки "Настройки" в инлайн меню
    """
    await callback.message.answer("/options", reply_markup=options_menu, disable_notification=True)
    await callback.answer()
