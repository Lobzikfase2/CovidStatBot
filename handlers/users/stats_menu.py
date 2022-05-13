from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.types import ReplyKeyboardRemove, InputFile

from handlers.users.region_set import set_region
from keyboards.default import more_menu, stats_menu
from keyboards.inline import get_started_markup
from loader import dp, db, gb
from utils.misc.misc import send_current_region_graphs, send_region_stats_of_the_day_real_time


@dp.message_handler(text="Мировая статистика")
async def world_stat(message: types.Message):
    """
    Действие бота при нажатии кнопки "Мировая статистика"
    """
    await send_region_stats_of_the_day_real_time(message, "world", "Мир")
    await send_current_region_graphs(message, "world", "- мировая статистика")


@dp.message_handler(text="Всероссийская статистика")
async def russia_stat(message: types.Message):
    """
    Действие бота при нажатии кнопки "Всероссийская статистика"
    """
    await send_region_stats_of_the_day_real_time(message, "russia", "Россия")
    await send_current_region_graphs(message, "russia", "- всероссийская статистика")


@dp.message_handler(text="Региональная статистика")
async def region_stat(message: types.Message):
    """
    Действие бота при нажатии кнопки "Региональная статистика"
    """
    user_id = message.chat.id
    region_id = db.region_is_set(user_id)
    if db.get_user(user_id) is None:
        db.add_user(user_id)
    if not region_id:
        await set_region(message)
    else:
        data = db.get_region_by_id(region_id)
        if data is not None:
            region_name = db.get_region_by_id(region_id)[1]
            await send_region_stats_of_the_day_real_time(message, region_id, f"<b>Регион: {region_name}</b>")
            await send_current_region_graphs(message, region_id, f"- {region_name}")
        else:
            await message.answer("<b>К сожалению, эта функция сейчас недоступна</b>")


@dp.message_handler(Text(startswith="Ещё"))
async def regions_comparison(message: types.Message):
    """
    Действие бота при нажатии кнопки "Ещё"
    """
    await message.answer("<i>ещё</i>", reply_markup=more_menu, disable_notification=True)


@dp.message_handler(Text(startswith="На главную"))
async def regions_comparison(message: types.Message):
    """
    Действие бота при нажатии кнопки "На главную"
    """
    await message.answer("<-", reply_markup=stats_menu, disable_notification=True,
                         parse_mode=types.ParseMode.MARKDOWN)


@dp.message_handler(Text(startswith="Сравнение"))
async def regions_comparison(message: types.Message):
    """
    Действие бота при нажатии кнопки "Сравнение регионов России по проценту смертности"
    """
    graph_path = await gb.get_regions_comparison()
    if graph_path is not None:
        await message.answer_photo(photo=InputFile(graph_path),
                                   caption="Сравнение регионов по проценту смертности")
    else:
        await message.answer("<b>К сожалению, эта функция сейчас недоступна</b>")


@dp.message_handler(text="Скрыть")
async def hide_menu(message: types.Message):
    """
    Действие бота при нажатии кнопки "Скрыть"
    """
    data = await message.answer("-", reply_markup=ReplyKeyboardRemove(), disable_notification=True)
    message_id = data['message_id']
    await dp.bot.delete_message(message.from_user.id, message_id)
    await message.answer("Давайте продолжим", reply_markup=get_started_markup, disable_notification=True)
