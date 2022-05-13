import aiohttp
import pandas as pd
from aiohttp import ClientConnectorError
from bs4 import BeautifulSoup as BS


async def async_request(url: str):
    """
    Осуществляет асинхронный запрос на сайт и возвращает текст ответа
    """
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, verify_ssl=False) as response:
                return await response.text()
        except ClientConnectorError:
            return None


async def get_regions_daily_stat(add_to_db=False, empty_cells_filler=0):
    """
    Возвращает статистику по всем регионам в текущий момент с сайта
    """
    # Делаем запрос на страницу
    # response = requests.get("https://coronavirus-monitor.info/#stats")
    # Делаем асинхронный запрос на страницу
    response = await async_request("https://coronavirus-monitor.info/#stats")
    if response is None:
        return None
    # Получаем объект класса BeautifulSoup для дальнейшей работы
    html = BS(response, "lxml")
    # Получаем список строк таблицы для дальнейшего перебора
    items = html.find(True, class_=["cut_tbl", "full_tbl"]).find_all(class_="flex-table")[1::]

    data = {'region': [],
            'confirmed': [],
            'confirmed_daily': [],
            'cured': [],
            'cured_daily': [],
            'deaths': [],
            'deaths_daily': [],
            'mortality_rate': []
            }

    for item in items:
        region = item.find('div')

        confirmed = region.find_next_sibling()
        confirmed_daily = confirmed.find("sup")
        if confirmed_daily:
            confirmed_daily.extract()
            confirmed_daily = confirmed_daily.text.replace("+", "")
        else:
            confirmed_daily = empty_cells_filler

        cured = confirmed.find_next_sibling()
        cured_daily = cured.find("sup")
        if cured_daily:
            cured_daily.extract()
            cured_daily = cured_daily.text.replace("+", "")
        else:
            cured_daily = empty_cells_filler

        deaths = cured.find_next_sibling()
        deaths_daily = deaths.find("sup")
        if deaths_daily:
            deaths_daily.extract()
            deaths_daily = deaths_daily.text.replace("+", "")
        else:
            deaths_daily = empty_cells_filler

        mortality_rate = deaths.find_next_sibling()
        mortality_rate = mortality_rate.text.replace("%", "")

        region = region.text
        confirmed = int(confirmed.text)
        confirmed_daily = int(confirmed_daily)
        cured = int(cured.text)
        cured_daily = int(cured_daily)
        deaths = int(deaths.text)
        deaths_daily = int(deaths_daily)
        mortality_rate = float(mortality_rate)

        data['region'].append(region)
        data['confirmed'].append(confirmed)
        data['confirmed_daily'].append(confirmed_daily)
        data['cured'].append(cured)
        data['cured_daily'].append(cured_daily)
        data['deaths'].append(deaths)
        data['deaths_daily'].append(deaths_daily)
        data['mortality_rate'].append(mortality_rate)

    df = pd.DataFrame(data)
    return df


async def russia_world_stat(url: str):
    """
    Вспомогательная функция для извлечения статистики по РФ и миру с сайта
    """
    response = await async_request(url)
    if response is None:
        return None
    html = BS(response, "lxml")
    items = html.find("div", class_="justify-content-center")
    err_str = "ожидание данных"
    if items is not None:
        confirmed = items.find(class_="confirmed")
        if confirmed is not None:
            confirmed_daily = confirmed.find("sup")
            if confirmed_daily is not None:
                confirmed_daily.extract()
            confirmed = int("".join(confirmed.text.replace("Заражено", "").split(" ")))
            if confirmed_daily is not None:
                confirmed_daily = int("".join(confirmed_daily.text.replace("+", "").split(" ")))
            else:
                confirmed_daily = 0
        else:
            confirmed = err_str
            confirmed_daily = 0

        cured = items.find(class_="cured")
        if cured is not None:
            cured_daily = cured.find("sup")
            if cured_daily is not None:
                cured_daily.extract()
            cured = int("".join(cured.text.replace("Вылечено", "").split(" ")))
            if cured_daily is not None:
                cured_daily = int("".join(cured_daily.text.replace("+", "").split(" ")))
            else:
                cured_daily = 0
        else:
            cured = err_str
            cured_daily = 0

        deaths = items.find(class_="deaths")
        if cured is not None:
            deaths_daily = deaths.find("sup")
            if deaths_daily is not None:
                deaths_daily.extract()
            deaths = int("".join(deaths.text.replace("Погибло", "").split(" ")))
            if deaths_daily is not None:
                deaths_daily = int("".join(deaths_daily.text.replace("+", "").split(" ")))
            else:
                deaths_daily = 0
        else:
            deaths = err_str
            deaths_daily = 0

        data_tuple = (confirmed, confirmed_daily, cured, cured_daily, deaths, deaths_daily)
    else:
        data_tuple = (err_str, err_str, err_str, err_str, err_str, err_str)
    return data_tuple


async def get_world_daily_stat():
    """
    Возвращает статистику по миру в текущий момент с сайта
    """
    return await russia_world_stat("https://coronavirus-monitor.info/#stats")


async def get_russia_daily_stat():
    """
    Возвращает статистику по РФ в текущий момент с сайта
    """
    return await russia_world_stat("https://coronavirus-monitor.info/country/russia/")


async def get_vaccination_stats():
    """
    Возвращает статистику о вакцинации в РФ в текущий момент с сайта
    """
    response = await async_request("https://xn--80aesfpebagmfblc0a.xn--p1ai/information/")
    if response is None:
        return None
    html = BS(response, "lxml")
    items = html.find("div", class_=["cv-stats-vaccine", "cv-grid"]).find_all("div", class_="cv-grid__item")
    data = ["".join((item.find("h3")).text.split(" ")) for item in items]
    data[0] = int(data[0])
    data[1] = int(data[1])
    data[2] = float(data[2].replace("%", "").replace(",", "."))
    return data
