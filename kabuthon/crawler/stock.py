# -*- coding: utf-8 -*-
from pyquery import PyQuery
import urllib
from datetime import datetime
import pandas as pd


def crawl_stock(code):
    opener = urllib.request.build_opener()
    url = f'https://info.finance.yahoo.co.jp/history/?code={code}.T'
    html = opener.open(url).read().decode("utf-8")
    q = PyQuery(html, parser='html')

    def get_table_row(index):
        return q(f".boardFin > tr > td:nth-child({index})")

    def to_date(dateText):
        year = int(dateText[:dateText.index("年")])
        month = int(dateText[dateText.index("年") + 1:dateText.index("月")])
        day = int(dateText[dateText.index("月") + 1:dateText.index("日")])
        return datetime(year, month, day)

    def to_float(numberText):
        return float(numberText.replace(",", ""))

    def to_int(numberText):
        return int(numberText.replace(",", ""))

    # TODO 株式の分割とかをうまく扱えるようにする
    invalid_rows = []
    for v, index in zip(get_table_row(2), range(len(get_table_row(2)))):
        try:
            to_float(v.text)
        except Exception:
            invalid_rows.append(index)

    def filter_invalid(elements):
        result = []
        for v, index in zip(elements, range(len(elements))):
            if index not in invalid_rows:
                result.append(v)
        return result

    dates = list(map(lambda a: to_date(a.text), filter_invalid(get_table_row(1))))
    opens = list(map(lambda a: to_float(a.text), filter_invalid(get_table_row(2))))
    heighs = list(map(lambda a: to_float(a.text), get_table_row(3)))
    lows = list(map(lambda a: to_float(a.text), get_table_row(4)))
    closes = list(map(lambda a: to_float(a.text), get_table_row(5)))
    volumes = list(map(lambda a: to_int(a.text), get_table_row(6)))
    adjust_close = list(map(lambda a: to_float(a.text), get_table_row(7)))
    return pd.DataFrame({'日付': dates, '始値': opens, '高値': heighs,
                         '安値': lows, '終値': closes, '出来高': volumes,
                         '調整後終値': adjust_close})
