import os
import sqlite3
from datetime import datetime
from pathlib import Path

from loader import db
from utils.misc.parsing import get_regions_daily_stat, get_world_daily_stat, get_russia_daily_stat


def clear_directory():
    """
    Очищает дерикторию, в которой хранятся графики
    """
    graphs = Path(Path.cwd(), "data", "graphs").glob("*.png")
    for graph in graphs:
        os.remove(graph)


async def daily_parse():
    """
    Собирает всю необходимую статистику для построения графиков и сохраняет её в БД
    """
    clear_directory()
    now_date = str(datetime.now().strftime("%Y-%m-%d"))
    world_stat = await get_world_daily_stat()
    russia_stat = await get_russia_daily_stat()
    all_regions_stat = await get_regions_daily_stat()
    if (world_stat is None) or (russia_stat is None) or (all_regions_stat is None):
        return

    try:
        db.add_stat_to_region("region_world", (now_date, *world_stat), regions=False)
    except sqlite3.IntegrityError as err:
        pass
    try:
        db.add_stat_to_region("region_russia", (now_date, *russia_stat), regions=False)
    except sqlite3.IntegrityError as err:
        pass

    for row_index in range(len(all_regions_stat.index)):
        try:
            row = all_regions_stat.iloc[row_index]
            region_id = db.get_region_by_name(row['region'])[0]
            data = (now_date, int(row['confirmed']), int(row['confirmed_daily']),
                    int(row['cured']), int(row['cured_daily']), int(row['deaths']),
                    int(row['deaths_daily']), float(row['mortality_rate']))
            db.add_stat_to_region('region_' + str(region_id), data, regions=True)
        except sqlite3.IntegrityError as err:
            pass
