from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.inline.callback_datas import get_started_callback

get_started_markup = InlineKeyboardMarkup(row_width=1,
                                          inline_keyboard=[
                                              [
                                                  InlineKeyboardButton(text="Статистика",
                                                                       callback_data=get_started_callback.new(
                                                                           "stats"))
                                              ],
                                              [
                                                  InlineKeyboardButton(text="Настройки",
                                                                       callback_data=get_started_callback.new(
                                                                           "options"))
                                              ]
                                          ])
