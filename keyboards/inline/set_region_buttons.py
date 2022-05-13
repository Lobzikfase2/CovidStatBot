from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_datas import region_callback, navigation_callback
from loader import db


def get_regions_markup(current_page: int = 0):
    """
    Функция генерирует инлайн меню с кнопками текущей страницы выбора региона
    """
    regions_list = db.get_all_regions()
    if regions_list is None:
        return None

    number_of_regions_on_page = 9
    left_bound = current_page * number_of_regions_on_page
    right_bound = (current_page + 1) * number_of_regions_on_page

    buttons_rows_list = []

    for region_id, region_name in regions_list[left_bound:right_bound]:
        row = [
            InlineKeyboardButton(text=region_name, callback_data=region_callback.new(id=region_id))]
        buttons_rows_list.append(row)

    navigation_row = []
    if current_page > 0:
        navigation_row.append(InlineKeyboardButton(text="⏪ назад",
                                                   callback_data=navigation_callback.new(type="backward",
                                                                                         current_page=current_page)))
    if (current_page + 1) * number_of_regions_on_page <= len(regions_list):
        navigation_row.append(InlineKeyboardButton(text="вперед ⏩",
                                                   callback_data=navigation_callback.new(type="forward",
                                                                                         current_page=current_page)))

    buttons_rows_list.append(navigation_row)

    return InlineKeyboardMarkup(inline_keyboard=buttons_rows_list)
