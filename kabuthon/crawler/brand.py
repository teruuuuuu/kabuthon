# -*- coding: utf-8 -*-
from pyquery import PyQuery


def get_brand(code):
    url = 'https://kabutan.jp/stock/?code={}'.format(code)
    q = PyQuery(url)
    if len(q.find('div.company_block')) == 0:
        return None
    try:
        name = q.find('div.company_block > h3').text()
        code_short_name = q.find('#stockinfo_i1 > div.si_i1_1 > h2').text()
        short_name = code_short_name[code_short_name.find(" ") + 1:]
        market = q.find('span.market').text()
        unit_str = q.find('#kobetsu_left > table:nth-child(4) > tbody > tr:nth-child(6) > td').text()
        unit = int(unit_str.split()[0].replace(',', ''))
        sector = q.find('#stockinfo_i2 > div > a').text()
    except (ValueError, IndexError):
        return None
    return code, name, short_name, market, unit, sector
