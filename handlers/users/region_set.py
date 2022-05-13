from aiogram import types

from keyboards.inline import get_regions_markup, get_started_markup
from keyboards.inline.callback_datas import region_callback, navigation_callback
from loader import dp, db


async def set_region(message: types.Message):
    """
    Присылыает пользователю инлайн меню с выбором региона
    """
    current_page = 0
    reply_markup = get_regions_markup(current_page)
    if reply_markup and reply_markup["inline_keyboard"] != [[]]:
        await message.answer("Выберите ваш регион из списка ⤵", reply_markup=get_regions_markup(current_page),
                             disable_notification=True)
    else:
        await message.answer("<b>К сожалению, эта функция сейчас недоступна</b>")


@dp.callback_query_handler(region_callback.filter())
async def region_tabbed(callback: types.CallbackQuery, callback_data: dict):
    """
    Действие бота при нажатии кнопки с нужным регионом в инлайн меню выбора региона
    """
    db.update_user_region(callback.message.chat.id, callback_data.get('id'))
    region_name = db.get_region_by_id(callback_data.get('id'))[1]
    await callback.message.delete()
    await dp.bot.send_message(chat_id=callback.message.chat.id, text=f"<b>Регион был изменён на: {region_name}</b>")
    await callback.message.answer("Давайте продолжим", reply_markup=get_started_markup, disable_notification=True)
    await callback.answer()


@dp.callback_query_handler(navigation_callback.filter())
async def change_page(callback: types.CallbackQuery, callback_data: dict):
    """
    Действие бота при нажатии кнопки перелистывания страницы
    в инлайн меню выбора региона
    """
    current_page = int(callback_data.get("current_page"))
    if callback_data.get("type") == "backward":
        current_page -= 1
    else:
        current_page += 1
    await callback.message.edit_reply_markup(reply_markup=get_regions_markup(current_page))
    await callback.answer(cache_time=0)
