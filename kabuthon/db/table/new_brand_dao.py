# -*- coding: utf-8 -*-

from db.connection import sql_execute
from db.connection import sql_executemany
from db.connection import count_sql

table_check_sql = """
        select count(1) 
        from sqlite_master 
        where type='table' 
            and name = 'new_brand'"""
create_sql = """
    create table new_brand (
        code TEXT PRIMARY_KEY
        , date TEXT
        , name TEXT)
    """

delete_all_sql = "delete from new_brand"


def insert_sql(code, date, name):
    return f"""
        INSERT INTO new_brand(code,date,name) 
        VALUES('{code}','{date}', '{name}')
    """


def select_by_code_sql(code):
    return f"""
        SELECT code, date, name from new_brand WHERE code = {code}
    """


def select_by_year_sql(year):
    return f"""
        SELECT code, date, name from new_brand WHERE date like '{year}%'
    """

class NewBrandDao:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(NewBrandDao, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def is_table_exist(self):
        return count_sql(table_check_sql) is not 0

    def create_table(self):
        if not self.is_table_exist():
            sql_execute(create_sql)

    def insert(self, code, date):
        sql_execute(insert_sql(code, date))

    def insert_many(self, newBrands):
        sql_executemany('INSERT INTO new_brand(code,date,name) VALUES(?,?,?)',
                        map(lambda newBrand: (newBrand.code, newBrand.date.strftime('%Y/%m/%d'), newBrand.name),
                            newBrands))

    def delete_all(self):
        sql_execute(delete_all_sql)

    def select_by_code(self, code):
        return sql_execute(select_by_code_sql(code))

    def select_by_year(self, year):
        return sql_execute(select_by_year_sql(year))