# -*- coding: utf-8 -*-

from db.connection import sql_execute
from db.connection import sql_executemany
from db.connection import count_sql

table_check_sql = """
        select count(1) 
        from sqlite_master 
        where type='table' 
            and name = 'price'"""
create_sql = """
    create table price (
        code TEXT 
        , date TEXT
        , open REAL
        , high REAL
        , low REAL
        , close REAL
        , volume INT
        , adjust_close REAL
        , PRIMARY KEY(code, date))
    """

delete_all_sql = "delete from price"


def insert_sql(code, date, op, high, low, close, volume, adjust_close):
    return f"""
        INSERT INTO price (code, date, open, high, low, close, volume, adjust_close) 
        VALUES('{code}','{date}', '{op}', '{high}', '{low}', '{close}', '{volume}', '{adjust_close}')
    """


def select_by_code_sql(code):
    return f"""
        SELECT code, date, open, high, low, close, volume, adjust_close from price WHERE code = '{code}'
    """

def select_by_code_date_sql(code, date):
    return f"""
        SELECT code, date, open, high, low, close, volume, adjust_close from price WHERE code = '{code}' AND date = '{date}'
    """

class PriceDao:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(PriceDao, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def is_table_exist(self):
        return count_sql(table_check_sql) is not 0

    def create_table(self):
        if not self.is_table_exist():
            sql_execute(create_sql)

    def insert(self, price):
        sql_execute(insert_sql(price))

    def insert_many(self, prices):
        sql_executemany("""
        INSERT INTO price(code, date, open, high, low, close, volume, adjust_close) 
        SELECT ?,?,?,?,?,?,?,?
        WHERE NOT EXISTS(SELECT 1 FROM price WHERE code = ? AND date = ?)""",
                        map(lambda price: (price.code, price.format_date(), price.open, price.high,
                                           price.low, price.close, price.volume, price.adjust_close,
                                           price.code, price.format_date()),
                            prices))

    def delete_all(self):
        sql_execute(delete_all_sql)

    def select_by_code(self, code):
        return sql_execute(select_by_code_sql(code))

    def select_by_code_date(self, code, date):
        return sql_execute(select_by_code_date_sql(code, date))
