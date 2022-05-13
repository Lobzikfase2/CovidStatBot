import asyncio
from datetime import datetime

from aiogram import executor

from loader import dp, db, scheduler
# Следующие два импорта обязательно должны присутствовать
# Они обновляют состояние объекта dp (Dispatcher)
# для его последующей передачи в метод start_polling()
# объекта executor
import middlewares, handlers
from utils.misc.parsing import get_regions_daily_stat
from utils.misc.scheduler import daily_parse, clear_directory
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands


async def on_startup(dispatcher):
    """
    Действия бота при старте работы
    """
    # Устанавливаем дефолтные команды
    await set_default_commands(dispatcher)

    # Уведомляет про запуск
    await on_startup_notify(dispatcher)


def start_scheduler(start_date: datetime):
    """
    Запуск ежедневного расписания
    :param start_date: дата старта
    """
    def inner_func():
        """
        Функция, которая будет запущена единовременно в указанную дату.
        Запускает функцию daily_parse(), добавляет её в расписание с интервалом запуска
        раз в сутки с момента запуска inner_func()
        """
        asyncio.new_event_loop().run_until_complete(daily_parse())
        scheduler.add_job(daily_parse, "interval", days=1)

    scheduler.add_job(inner_func, "date", run_date=start_date, timezone='Europe/Moscow')
    scheduler.start()


if __name__ == '__main__':
    # Создаём таблицу пользователей
    db.create_table_users()
    # Создаём таблицу-список регионов
    db.create_table_regions()
    # Предварительно очищаем таблицу регионов
    db.delete_all_regions()

    # Заполняем таблицу регионов списком регионов, полученных с сайта
    regions_daily_stat_dt = asyncio.get_event_loop().run_until_complete(get_regions_daily_stat())
    if regions_daily_stat_dt is not None:
        db.add_regions(regions_daily_stat_dt["region"].to_list())
        db.create_region_tables()

    # Очищаем директорию с картинками графиков
    clear_directory()

    # Запускаем ежедневный сбор статистики
    now_date = datetime.now().date()
    start_time = datetime(now_date.year, now_date.month, now_date.day, 23, 59)
    start_scheduler(start_time)

    # Запуск бота
    executor.start_polling(dp, on_startup=on_startup)
