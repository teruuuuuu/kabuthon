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
    create table brand (
        code TEXT PRIMARY_KEY
        , name TEXT
        , short_name TEXT
        , market TEXT
        , sector TEXT
        , unit INT)
    """
delete_all_sql = "delete from brand"
select_all_sql = "select code, name, short_name, market, sector, unit from brand"


def insert_sql(code, name, short_name, market, sector, unit):
    return f"""
        INSERT INTO brand(code,name,short_name,market,unit,sector) 
        VALUES({code},{name},{short_name},{market},{sector},{unit})
    """

def delete_by_code_sql(code):
    return f"DELETE FROM brand WHERE code = '{code}'"

def select_by_code_sql(code):
    return f"""
        SELECT code, name, short_name, market, sector, unit from brand WHERE code = {code}
    """

class BrandDao:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(BrandDao, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def is_table_exist(self):
        return count_sql(table_check_sql) is not 0

    def create_table(self):
        if not self.is_table_exist():
            sql_execute(create_sql)

    def insert(self, code, name, short_name, market, sector, unit):
        sql_execute(insert_sql(code=code, name=name, short_name=short_name,
                               market=market, sector=sector, unit=unit))

    def insert_many(self, brands):
        sql_executemany('INSERT INTO brand(code,name,short_name,market,unit,sector) VALUES(?,?,?,?,?,?)',
                        map(lambda brand: (brand.code, brand.name, brand.short_name,
                                           brand.market, brand.unit, brand.sector), brands))

    def delete_all(self):
        sql_execute(delete_all_sql)

    def delete_by_code(self, code):
        sql_execute(delete_by_code_sql(code))


    def select_all(self):
        return sql_execute(select_all_sql)

    def select_by_code(self, code):
        return sql_execute(select_by_code_sql(code))

