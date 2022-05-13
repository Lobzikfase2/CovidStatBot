import sqlite3

from typing import List


class Database:
    """
    Класс Database используется для взаимодействия с БД в ООП парадигме
    """
    def __init__(self, path="main.db", logging=False):
        self.path = path
        self.logging = logging

    @property
    def connection(self):
        """
        Создаёт и возвращает объект соединения с БД
        """
        return sqlite3.connect(self.path)

    def execute(self, sql: str, parameters: tuple = None, fetch_one=False,
                fetch_all=False, commit=False):
        """
        Выполнить SQL запрос
        """
        if not parameters:
            parameters = tuple()
        connection = self.connection
        if self.logging:
            connection.set_trace_callback(logger)
        cursor = connection.cursor()
        cursor.execute(sql, parameters)

        data = None
        if commit:
            connection.commit()
        if fetch_one:
            data = cursor.fetchone()
        if fetch_all:
            data = cursor.fetchall()

        connection.close()
        return data

    def create_table_users(self):
        """
        Создаёт таблицу пользователей
        """
        sql = """
        CREATE TABLE IF NOT EXISTS users (
        id int NOT NULL,
        region_id int DEFAULT NULL,
        interval int DEFAULT 3,
        stats_type int DEFAULT 1,
        PRIMARY KEY (id)
        )
        """

        self.execute(sql, parameters=(), commit=True)

    def create_table_regions(self):
        """
        Создаёт таблицы регионов
        """
        sql = """
        CREATE TABLE IF NOT EXISTS regions(
        id int NOT NULL,
        region varchar(255) DEFAULT NULL,
        PRIMARY KEY (region) 
        )
        """
        self.execute(sql, parameters=(), commit=True)

    def create_region_tables(self):
        """
        Создаёт таблицу со списком регионов
        """
        sql = """
                         CREATE TABLE IF NOT EXISTS {0} (
                         date NUMERIC,
                         confirmed INTEGER,
                         confirmed_daily INTEGER,
                         cured INTEGER,
                         cured_daily INTEGER,
                         deaths INTEGER,
                         deaths_daily INTEGER,
                         PRIMARY KEY (date)
                         )
                        """
        self.execute(sql.format(f"region_world"), parameters=(), commit=True)
        self.execute(sql.format(f"region_russia"), parameters=(), commit=True)

        sql = """
                 CREATE TABLE IF NOT EXISTS {0} (
                 date NUMERIC,
                 confirmed INTEGER,
                 confirmed_daily INTEGER,
                 cured INTEGER,
                 cured_daily INTEGER,
                 deaths INTEGER,
                 deaths_daily INTEGER,
                 mortality_rate FLOAT, 
                 PRIMARY KEY (date)
                 )
                """
        for id, region in self.get_all_regions():
            self.execute(sql.format(f"region_{id}"), parameters=(), commit=True)

    def add_user(self, id: int):
        """
        Добавить пользователя в таблицу
        """
        sql = "INSERT INTO users(id) VALUES(?)"
        parameters = (id,)
        self.execute(sql, parameters, commit=True)

    def update_user_region(self, user_id, region_id: int):
        """
        Обновить регион пользователя
        """
        print(f"Updating... user_id: {user_id}, region_id: {region_id}")
        sql = "UPDATE users SET region_id = ? WHERE id = ?"
        parameters = (region_id, user_id)
        self.execute(sql, parameters, commit=True)

    def update_user_interval(self, user_id, interval: int):
        """
        Обновить пользовательские настройки
        интервала отображения статистики
        """
        sql = "UPDATE users SET interval = ? WHERE id = ?"
        parameters = (interval, user_id)
        self.execute(sql, parameters, commit=True)

    def update_user_stats_type(self, user_id, stats_type: int):
        """
        Обновить пользовательские настройки
        типа статистических данных,
        отображаемых на графике
        """
        sql = "UPDATE users SET stats_type = ? WHERE id = ?"
        parameters = (stats_type, user_id)
        self.execute(sql, parameters, commit=True)

    def get_user(self, user_id):
        """
        Возвращает данные о пользователе из БД
        """
        sql = "SELECT * FROM users WHERE id=?"
        return self.execute(sql, parameters=(user_id,), fetch_one=True)

    def region_is_set(self, user_id):
        """
        Проверяет задан ли у пользователя регион и возвращает его,
        в случае его наличия в БД
        """
        sql = "SELECT region_id FROM users WHERE id=?"
        region_id = self.execute(sql, parameters=(user_id,), fetch_one=True)
        if region_id:
            region_id = region_id[0]
        if type(0) == type(region_id) and 1 <= region_id <= 85:
            return region_id
        return None

    def add_stat_to_region(self, region_name, data, regions):
        """
        Добавляет статистику по региону в БД
        """
        if regions:
            sql = f"INSERT INTO {region_name} VALUES(?, ?, ?, ?, ?, ?, ?, ?)"
        else:
            sql = f"INSERT INTO {region_name} VALUES(?, ?, ?, ?, ?, ?, ?)"
        self.execute(sql, data, commit=True)

    def add_regions(self, regions: List[str]):
        """
        Добавляет список всех существующих регионов РФ в БД
        """
        sql = "INSERT INTO regions(id, region) VALUES(?, ?)"
        for i in range(len(regions)):
            parameters = (i + 1, regions[i])
            self.execute(sql, parameters, commit=True)

    def delete_all_regions(self):
        """
        Очищает таблицу регионов
        """
        self.execute("DELETE FROM regions WHERE True", commit=True)

    def get_all_regions(self):
        """
        Возвращает список всех существующих регионов РФ, записанных в БД
        """
        sql = "SELECT * FROM regions"
        try:
            data = self.execute(sql, parameters=(), fetch_all=True)
            if not data:
                return None
            return data
        except sqlite3.OperationalError:
            return None

    def get_region_by_id(self, region_id):
        """
        Возвращает id и название региона по его id в БД в таблице regions
        """
        sql = "SELECT * FROM regions WHERE id=?"
        return self.execute(sql, parameters=(region_id,), fetch_one=True)

    def get_region_by_name(self, region_name):
        """
        Возвращает id и название региона по его названию в БД в таблице regions
        """
        sql = "SELECT * FROM regions WHERE region=?"
        return self.execute(sql, parameters=(region_name,), fetch_one=True)

    def get_region_stats(self, region_id, with_mortality_rate=False):
        """
        Возвращает статистику по конкретному региону
        """
        sql = "SELECT date, confirmed, confirmed_daily, cured," \
              " cured_daily, deaths, deaths_daily from {0}"
        if with_mortality_rate:
            sql = "SELECT date, confirmed, confirmed_daily, cured, cured_daily," \
                  " deaths, deaths_daily, mortality_rate from {0}"
        try:
            data = self.execute(sql.format("region_" + str(region_id)), fetch_all=True)
            if not data:
                return None
            return data
        except sqlite3.OperationalError:
            return None


def logger(statement):
    """
    Задаёт способ логиррования взаимодействий с БД
    """
    print(f"""
    -------------Executing:------------
    {statement}
    -----------------------------------
    """)
