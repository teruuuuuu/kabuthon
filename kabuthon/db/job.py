# -*- coding: utf-8 -*-
from db.connection import DbConnection
from db.table.brand_dao import BrandDao
from db.table.new_brand_dao import NewBrandDao
from db.table.price_dao import PriceDao


def setup():
    print("migration start")
    with DbConnection().exclusive():
        BrandDao().create_table()
        NewBrandDao().create_table()
        PriceDao().create_table()
    print("migration end")