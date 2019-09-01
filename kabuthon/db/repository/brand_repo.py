# -*- coding: utf-8 -*-
from functools import reduce
from itertools import chain
from datetime import datetime, timedelta
from operator import add

from db.connection import DbConnection
from db.entity.brand import Brand
from db.entity.new_brand import NewBrand
from db.entity.price import Price
from db.table.brand_dao import BrandDao
from db.table.new_brand_dao import NewBrandDao
from db.table.price_dao import PriceDao


class BrandRepo:
    _instance = None
    conn = None
    brand_dao = None
    new_brand_dao = None
    price_dao = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            print("brand repo new")
            cls._instance = super(BrandRepo, cls).__new__(cls, *args, **kwargs)
            cls.conn = DbConnection()
            cls._instance.brand_dao = BrandDao()
            cls._instance.new_brand_dao = NewBrandDao()
            cls._instance.price_dao = PriceDao()
        return cls._instance

    def setup(self):
        with self.conn.exclusive():
            self.brand_dao.create_table()
            self.new_brand_dao.create_table()

    def insert_brands(self, brands):
        with self.conn.exclusive():
            insert_data = list(filter(
                lambda brand: not self.brand_dao.select_by_code(brand.code).fetchone(), brands))
            self.brand_dao.insert_many(insert_data)

    def insert_new_brands(self, new_brands):
        with self.conn.exclusive():
            insert_data = list(filter(
                lambda new_brand: not self.new_brand_dao.select_by_code(new_brand.code).fetchone(), new_brands))
            self.new_brand_dao.insert_many(insert_data)

    def insert_stocks(self, stocks):
        with self.conn.auto_commit():
            self.price_dao.insert_many(stocks)

    def delete_all(self):
        with self.conn.exclusive():
            self.brand_dao.delete_all()
            self.new_brand_dao.delete_all()
            self.price_dao.delete_all()

    def delete_brand_by_codes(self, codes):
        for code in codes:
            with self.conn.auto_commit():
                self.brand_dao.delete_by_code(code)


    def select_new_brand_recently(self):
        this_year = datetime.now().year
        last_year = this_year - 1
        with self.conn.exclusive():
            return chain(
                map(lambda new_brand: NewBrand(new_brand[0], new_brand[1], new_brand[2]),
                    self.new_brand_dao.select_by_year(this_year)),
                map(lambda new_brand: NewBrand(new_brand[0], new_brand[1], new_brand[2]),
                    self.new_brand_dao.select_by_year(last_year)))

    def select_all_brand(self):
        with self.conn.exclusive():
            return map(lambda brand: Brand(brand[0], brand[1], brand[2], brand[3], brand[4], brand[5]),
                       self.brand_dao.select_all())

    def select_prices_recently(self, code):
        day_base = datetime.now() - timedelta(days=1)
        days = list(map(lambda d: (day_base - timedelta(days=d)).strftime('%Y/%m/%d'), range(14)))

        prices = list(map(lambda p: Price(p[0], datetime.strptime(p[1], '%Y/%m/%d'),
                                          p[2], p[3], p[4], p[5], p[6], p[7]),
                          reduce(add, list(map(lambda d: list(self.price_dao.select_by_code_date(code, d)), days)))))
        prices.reverse()
        return prices

    def select_prices(self, code):
        prices = list(map(lambda p: Price(p[0], datetime.strptime(p[1], '%Y/%m/%d'), p[2], p[3], p[4], p[5], p[6], p[7]),
                 list(self.price_dao.select_by_code(code))))
        return sorted(prices, key=lambda p: p.date)

    def select_brand_by_code(self, code):
        brands = list(self.brand_dao.select_by_code(code))
        return Brand(brands[0][0], brands[0][1], brands[0][2], brands[0][3], brands[0][4], brands[0][5]) \
            if len(brands) > 0 else None
