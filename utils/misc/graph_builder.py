import asyncio
import concurrent
import os
from utils.db_api.sqlite import Database
import enum
from datetime import datetime
import pandas as pd
import plotly.express as px
from pathlib import Path
import locale
from functools import partial

from utils.misc.parsing import get_regions_daily_stat


class GraphPeriod(enum.Enum):
    """
    Класс GraphPeriod являтся пользателским перечислением,
    отражающим выбранный интервал показа статистики на графиках
    """
    ForTheMonth = {'title': "за последний месяц", "type": "month"}
    ForTheYear = {'title': "за последний год", "type": "year"}
    AllTime = {'title': "за всё время", "type": "alltime"}


class StatsType(enum.Enum):
    """
    Класс StatsType являтся пользателским перечислением,
    отражающим выбранный тип статистических данных,
    отображаемых на графике
    """
    Confirmed = {"type": "confirmed", "color": "blue", 'title': "Общее число заражений", 'y_axis_title': "Заражений"}
    ConfirmedDaily = {"type": "confirmed_daily", "color": "blue", 'title': "Прирост заражений за день",
                      'y_axis_title': "Заражений за день"}
    Cured = {"type": "cured", "color": "green", 'title': "Общее число выздоровлений", 'y_axis_title': "Выздоровлений"}
    CuredDaily = {"type": "cured_daily", "color": "green", 'title': "Прирост выздоровлений за день",
                  'y_axis_title': "Выздоровлений за день"}
    Deaths = {"type": "deaths", "color": "red", 'title': "Общее число смертей", 'y_axis_title': "Смертей"}
    DeathsDaily = {"type": "deaths_daily", "color": "red", 'title': "Прирост смертей за день",
                   'y_axis_title': "Смертей за день"}


class GraphBuilder:
    """
    Класс GraphBuilder используется для построения всех типов графиков,
    предоставляемых ботом
    """

    def __init__(self, db: Database):
        self.db = db

    async def get_regions_comparison(self):
        """
        Создаёт график сравнения регионов РФ по проценту смертности
        """
        file_name = "regions_comparison.png"
        file_path = Path(Path.cwd(), "data", "graphs", file_name)
        if os.path.exists(file_path):
            return file_path

        df = await get_regions_daily_stat()
        if df is None:
            return None
        df = df.sort_values(by="mortality_rate", ascending=False)

        fig = px.bar(df, x="region", y="mortality_rate",
                     color="mortality_rate",
                     title="<b>Процент смертности</b> от заболевания коронавирусом<br>по следующим регионам",
                     template="plotly_dark+presentation+xgridoff",
                     labels={"mortality_rate": ""}
                     )

        fig.update_layout(yaxis_title="Процент смертности %",
                          xaxis=dict(title="", tickfont=dict(size=16)),
                          title={'font': dict(size=36), 'x': 0.5},
                          showlegend=False)

        write_image_frozen_kwargs = partial(fig.write_image, scale=2, width="1920", height="1080")
        await run_blocking_io(write_image_frozen_kwargs, file_path)
        return file_path

    async def get_region_stats(self, region_id="world", stats_type: StatsType = StatsType.Confirmed,
                         period: GraphPeriod = GraphPeriod.AllTime):
        """
        Создаёт графики со статистикой подтверждённых случаев
        :param region_id: выбранный регоин
        :param stats_type: тип статистики (Confirmed, ConfirmedDaily, Cured, CuredDaily, Deaths, DeathsDaily)
        :param period: временной интервал отображаемых на графике данных (ForTheMonth, ForTheYear, AllTime)
        """
        file_name = 'region_' + str(region_id) + "_" + stats_type.value['type'] + "_" + period.value['type'] + ".png"
        file_path = Path(Path.cwd(), "data", "graphs", file_name)

        if os.path.exists(file_path):
            return file_path
        else:
            data = self.db.get_region_stats(region_id)
            if data is None:
                return None
            df = pd.DataFrame(data)
            df.columns = ["date", "confirmed", "confirmed_daily",
                          "cured", "cured_daily", "deaths",
                          "deaths_daily"]

            if period == GraphPeriod.ForTheMonth:
                df = df.tail(30)
            elif period == GraphPeriod.ForTheYear:
                df = df.tail(365)

            min_val = df[stats_type.value['type']].min()
            max_val = df[stats_type.value['type']].max()
            offset = int((max_val - min_val) / 4)
            min_y = min_val - offset
            if min_y < 0:
                min_y = 0
            max_y = max_val + offset
            if region_id == "world":
                graph_title = "Мир | "
            elif region_id == "russia":
                graph_title = "Россия | "
            else:
                graph_title = self.db.get_region_by_id(region_id)[1] + " | "
            graph_title += stats_type.value['title'] + " | Данные " + period.value['title']

            fig = px.area(df, x="date", y=stats_type.value['type'],
                          color_discrete_sequence=[stats_type.value['color']],
                          title=graph_title,
                          template="plotly_white"
                          )

            if period == GraphPeriod.ForTheMonth:
                locale.setlocale(locale.LC_ALL, "ru_RU.utf8")
                tick_text = [datetime.strptime(str(df['date'][elem_index]), "%Y-%m-%d").strftime('%B-%d')
                             for elem_index in df.index]
                fig.update_xaxes(tickformat='%B')
                fig.update_xaxes(tickvals=df['date'])
                fig.update_xaxes(ticktext=tick_text)
            locale.setlocale(locale.LC_ALL, "en_US.utf8")
            fig.update_xaxes(
                tickformatstops=[
                    dict(dtickrange=[None, 86400000], value="%b %d\n%Y")
                ])

            fig.update_layout(yaxis_range=[min_y, max_y])
            fig.update_layout(yaxis=dict(title=f"{stats_type.value['y_axis_title']}", titlefont=dict(size=20),
                                         tickfont=dict(size=16)),
                              xaxis=dict(title="", tickfont=dict(size=16)),
                              title={'font': dict(size=36), 'x': 0.5},
                              showlegend=False,
                              )

            write_image_frozen_kwargs = partial(fig.write_image, scale=2, width="1920", height="1080")
            await run_blocking_io(write_image_frozen_kwargs, file_path)
            return file_path


async def run_blocking_io(func, *args):
    """
    Служит для запуска функций, блокируемых IO операциями, асинхронно
    """
    loop = asyncio.get_running_loop()
    with concurrent.futures.ThreadPoolExecutor() as pool:
        result = await loop.run_in_executor(
            pool, func, *args
        )
    return result
