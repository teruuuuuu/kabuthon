# -*- coding: utf-8 -*-
import time
from functools import reduce
from itertools import chain
from operator import add

from crawler.new_brand import get_new_brands2
from crawler.brand import get_brand
from crawler.stock import crawl_stock
from db.entity.brand import Brand
from db.entity.new_brand import NewBrand
from db.entity.price import Price
from db.repository.brand_repo import BrandRepo


def save_newbrand():
    BrandRepo().insert_new_brands(list(map(
        lambda new_brand: NewBrand(new_brand[0], new_brand[1].strftime('%Y/%m/%d'), new_brand[2]),
        get_new_brands2())))


def sync_brand():
    def read_brand_codes(filepath):
        with open(filepath) as f:
            return filter(lambda code: code != '', map(lambda code: code.strip(), f.read().split("\n")))

    def crawl_brands(new_codes):
        for new_code in new_codes:
            brand = get_brand(new_code)
            print(brand)
            yield Brand(brand[0], brand[1], brand[2], brand[3], brand[5], brand[4])
            time.sleep(3)

    print("sync brand start")
    target_codes_set = set(read_brand_codes("brand_list.txt"))
    saved_codes_set = set(map(lambda brand: brand.code, BrandRepo().select_all_brand()))
    new_codes = filter(lambda target_code: target_code not in saved_codes_set, target_codes_set)
    del_codes = filter(lambda saved_code: saved_code not in target_codes_set, saved_codes_set)
    BrandRepo().insert_brands(list(crawl_brands(new_codes)))
    BrandRepo().delete_brand_by_codes(list(del_codes))
    print("sync brand end")


def save_stock():
    def crawl(code):
        time.sleep(3)
        return map(lambda l: Price(code, l[0].to_pydatetime(), l[1], l[2], l[3], l[4], l[5], l[6]),
                   crawl_stock(code).values.tolist())
    print("save stock start")
    # TODO 一旦全レコード分メモリ展開するのは直す
    BrandRepo().insert_stocks(
        reduce(add, list(map(lambda brand: list(crawl(brand.code)), list(BrandRepo().select_all_brand())))))
    print("save stock end")