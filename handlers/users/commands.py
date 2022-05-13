import logging
import sqlite3

import aiohttp
from aiogram import types
from aiogram.dispatcher.filters.builtin import Command, CommandHelp
from aiogram.dispatcher.filters.builtin import CommandStart

from keyboards.default import stats_menu, options_menu
from keyboards.inline import get_started_markup
from loader import dp, db


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    """
    Функция - обработчик команды /start
    """
    user_id = message.chat.id
    try:
        db.add_user(user_id)
    except sqlite3.IntegrityError as err:
        logging.info(f"Пользователь с id: {user_id} уже есть в базе")
    photo_url = "https://www.boredpanda.com/blog/wp-content/uploads/" \
                "2020/03/Iranian-artist-makes-impactful-cartoons-to-reflect-on-the-coronavirus-5e81909a523c8__880.jpg"
    async with aiohttp.ClientSession() as session:
        async with session.get(photo_url, verify_ssl=False) as response:
            if response.status == 200:
                exclamation_mark = f"<a href='{photo_url}'>!</a>"
            else:
                exclamation_mark = "!"

    await message.answer(f"<b>Привет{exclamation_mark}</b> Я — бот для просмотра \n"
                         f"статистики по <u>коронавирусу</u> 🦠\n\n"
                         f"С помощью меня, ты сможешь мгновенно узнать любую, \n"
                         f"интересующую тебя информацию по болезни. \n\n"
                         f"<b><i>Что я умею?</i></b>\n"
                         f"    - показывать мировую и \n"
                         f"      всероссийскую статистику 🌍\n\n"
                         f"    - предоставлять как данные за \n"
                         f"      всё время развития вируса, \n"
                         f"      так и информацию за \n"
                         f"      текущий день 🕑\n\n"
                         f"    - в зависимости от вашего \n"
                         f"      региона, я могу показать вам \n"
                         f"      статистику именно по вашему\n"
                         f"      месту жительства 📪\n\n"
                         f"<b>Команды:</b>\n"
                         f"    - статистика: /stats\n"
                         f"    - настройки: /options\n"
                         f"    - помощь: /help\n",
                         reply_markup=get_started_markup)


@dp.message_handler(Command("stats"))
async def show_menu(message: types.Message):
    """
    Функция - обработчик команды /stats
    """
    await message.answer("/stats", reply_markup=stats_menu, disable_notification=True)


@dp.message_handler(Command("options"))
async def change_region(message: types.Message):
    """
    Функция - обработчик команды /options
    """
    await message.answer("/options", reply_markup=options_menu, disable_notification=True)


@dp.message_handler(CommandHelp())
async def change_region(message: types.Message):
    """
    Функция - обработчик команды /help
    """
    await message.answer('<b>Справка</b>\n\n'
                         ''
                         'Кнопка "Статистика" открывает \n'
                         'меню показа статистики.\n\n'
                         ''
                         'Выберете желаемую зону охвата земного шара:\n'
                         '   1) Мировая статистика \n'
                         '         - данные со всего мира\n'
                         '   2) Всероссийская статистика \n'
                         '         - данные со всей России\n'
                         '   3) Региональная статистика \n'
                         '         - данные из выбранного \n'
                         '            в настройках региона\n'
                         '   4) Прочая статистика, \n'
                         '        по нажатию кнопки "Ещё"\n'
                         '---------------------------------------\n'
                         '<i>Если вы ещё не выбрали ваш регион, \n'
                         'то при попытке получить региональную статистику, \n'
                         'вы увидите окно, \n'
                         'в котором сможете его выбрать. \n'
                         '(изменить регион будет можно в любой момент)</i>\n'
                         '---------------------------------------\n'
                         'Кнопка "Настройки" открывает \n'
                         'меню настроек. \n\n'
                         ''
                         'Вы можете:\n'
                         '    - изменить ваш регион\n'
                         '    - настроить типы графиков, \n'
                         '       которые вы будете получать\n'
                         '---------------------------------------\n'
                         'Настройки графиков. \n\n'
                         ''
                         'Вам доступен:\n'
                         '    - выбор временного промежутка \n'
                         '       отображения статистики:\n'
                         '		           а) За последний месяц\n'
                         '             б) За последний год\n'
                         '             в) За всё время\n\n'
                         ''
                         '    - выбор типа отображаемых \n'
                         '       на графике данных :\n'
                         '		           a) Общее число случаев \n'
                         '                  на момент каждого дня \n'
                         '                  ("накопительная" \n'
                         '                  статистика)\n\n'
                         ''

                         '             б) Прирост числа случаев \n'
                         '                  за каждый конкретный \n'
                         '                  день\n\n'
                         '---------------------------------------',
                         reply_markup=get_started_markup)
