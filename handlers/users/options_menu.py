from aiogram import types
from aiogram.types import ReplyKeyboardRemove

from handlers.users.region_set import set_region
from keyboards.default import graphs_options
from loader import dp


@dp.message_handler(text="Изменить регион")
async def region_stats(message: types.Message):
    """
    Действия бота, при нажатии кнопки "Изменить регион"
    """
    await message.answer("<i>изменение региона</i>", reply_markup=ReplyKeyboardRemove(), disable_notification=True)
    await set_region(message)


@dp.message_handler(text="Настройки отображения графиков")
async def region_stats(message: types.Message):
    """
    Действия бота, при нажатии кнопки "Настройки отображения графиков"
    """
    await message.answer("<i>настройки отображения графиков</i>", reply_markup=graphs_options,
                         disable_notification=True)
