import asyncio
import concurrent.futures
import locale
from datetime import datetime

import pandas as pd
from aiogram import types
from aiogram.types import InputFile, MediaGroup

from loader import db, gb
from utils.misc import GraphPeriod, StatsType
from utils.misc.parsing import get_vaccination_stats, get_world_daily_stat, get_russia_daily_stat, \
    get_regions_daily_stat


async def send_region_stats_of_the_day_real_time(message: types.Message, region_id, region_text: str = ""):
    """
    Отправляет пользователю статистику по текушему дню в заданном регионе в реальном времени
    """
    if str(region_id) == "world":
        data = await get_world_daily_stat()
    elif str(region_id) == "russia":
        data = await get_russia_daily_stat()
    else:
        data = await get_regions_daily_stat()
        if data is not None:
            id = str(region_id).replace("region_id", "")
            region_name = db.get_region_by_id(id)[1]
            data = list(data.loc[data['region'] == region_name].iloc[0])[1:]

    if data is not None:
        locale.setlocale(locale.LC_ALL, "ru_RU.utf8")
        date = datetime.now().strftime('%d %B %Y')
        locale.setlocale(locale.LC_ALL, "en_US.utf8")

        text = f"<b>{region_text} | {date}</b>\n" \
               f"Общее число заражений: \n" \
               f"{data[0]}\n" \
               f"За сутки: +{data[1]}\n\n" \
               f"Общее число выздоровлений: \n" \
               f"{data[2]}\n" \
               f"За сутки: +{data[3]}\n\n" \
               f"Общее число смертей: \n" \
               f"{data[4]}\n" \
               f"За сутки: +{data[5]}\n\n"

        if region_id == "russia":
            data = await get_vaccination_stats()
            if data is not None:
                text += f"Вакцинацировано первым компонентом: {data[0]}\n"
                text += f"Вакцинацировано вторым компонентом: {data[1]}\n"
                text += f"Коллективный иммунитет: {data[2]}%\n"

        if region_id != "world" and region_id != "russia":
            text += f"Процент смертности: {data[6]}%"

        await message.answer(text)


async def send_region_stats_of_the_day(message: types.Message, region_id, region_text: str = ""):
    """
    Отправляет пользователю статистику по последней записе из БД в заданном регионе
    """
    if str(region_id) == "world" or str(region_id) == "russia":
        data = db.get_region_stats(region_id)
    else:
        data = db.get_region_stats(region_id, with_mortality_rate=True)
    if data is not None and data != []:
        stats_names_list = ["date", "confirmed", "confirmed_daily",
                            "cured", "cured_daily", "deaths",
                            "deaths_daily"]
        if region_id != "world" and region_id != "russia":
            stats_names_list.append("mortality_rate")

        df_last_day = pd.Series(data[-1])
        df_before_last_day = pd.Series(data[-2])
        df_last_day.index = stats_names_list
        df_before_last_day.index = stats_names_list

        locale.setlocale(locale.LC_ALL, "ru_RU.utf8")
        date = datetime.strptime(str(df_before_last_day['date']), "%Y-%m-%d").strftime('%d %B %Y')
        locale.setlocale(locale.LC_ALL, "en_US.utf8")

        text = f"<b>{region_text} | {date}</b>\n" \
               f"Общее число заражений: \n" \
               f"{df_before_last_day['confirmed']}\n" \
               f"За сутки: +{df_before_last_day['confirmed_daily']}\n\n" \
               f"Общее число выздоровлений: \n" \
               f"{df_before_last_day['cured']}\n" \
               f"За сутки: +{df_before_last_day['cured_daily']}\n\n" \
               f"Общее число смертей: \n" \
               f"{df_before_last_day['deaths']}\n" \
               f"За сутки: +{df_before_last_day['deaths_daily']}\n\n"

        if region_id == "russia":
            data = await get_vaccination_stats()
            if data is not None:
                text += f"Вакцинацировано первым компонентом: {data[0]}\n"
                text += f"Вакцинацировано вторым компонентом: {data[1]}\n"
                text += f"Коллективный иммунитет: {data[2]}%\n"

        if region_id != "world" and region_id != "russia":
            text += f"Процент смертности: {df_before_last_day['mortality_rate']}%"

        await message.answer(text)


async def send_current_region_graphs(message: types.Message, region_id, caption=""):
    """
    Отправляет пользователю графики со статистикой по заданному региону
    """
    user_id, region_id_from_bd, interval, stats_type = db.get_user(message.chat.id)
    caption += "\n"
    if interval == 1:
        interval = GraphPeriod.ForTheMonth
        caption += "{0} за месяц"
    elif interval == 2:
        interval = GraphPeriod.ForTheYear
        caption += "{0} за год"
    else:
        interval = GraphPeriod.AllTime
        caption += "{0} за всё время"
    album = MediaGroup()
    if stats_type == 1:
        caption = caption.format("- прирость случаев за день \n- данные")
        graph1_path = await gb.get_region_stats(region_id, period=interval, stats_type=StatsType.ConfirmedDaily)
        graph2_path = await gb.get_region_stats(region_id, period=interval, stats_type=StatsType.CuredDaily)
        graph3_path = await gb.get_region_stats(region_id, period=interval, stats_type=StatsType.DeathsDaily)
        if graph1_path is None or graph2_path is None or graph3_path is None:
            await message.answer("<b>К сожалению, эта функция сейчас недоступна</b>")
        else:
            album.attach_photo(InputFile(graph1_path))
            album.attach_photo(InputFile(graph2_path))
            album.attach_photo(InputFile(graph3_path), caption=caption)
            await message.answer_media_group(album)

    else:
        caption = caption.format("- общее число случаев \n- данные")
        graph1_path = await gb.get_region_stats(region_id, period=interval, stats_type=StatsType.Confirmed)
        graph2_path = await gb.get_region_stats(region_id, period=interval, stats_type=StatsType.Cured)
        graph3_path = await gb.get_region_stats(region_id, period=interval, stats_type=StatsType.Deaths)
        if graph1_path is None or graph2_path is None or graph3_path is None:
            await message.answer("<b>К сожалению, эта функция сейчас недоступна</b>")
        else:
            album.attach_photo(InputFile(graph1_path))
            album.attach_photo(InputFile(graph2_path))
            album.attach_photo(InputFile(graph3_path), caption=caption)

            await message.answer_media_group(album)



