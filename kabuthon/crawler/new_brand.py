# -*- coding: utf-8 -*-
import urllib

from pyquery import PyQuery
from datetime import datetime


def get_new_brands():
    url = 'http://www.jpx.co.jp/listing/stocks/new/index.html'
    q = PyQuery(url)
    for d, i in zip(q.find('tbody > tr:even > td:eq(0)'),
                    q.find('tbody > tr:even span')):
        date = datetime.strptime(d.text, '%Y/%m/%d').date()
        yield (i.get('id'), date)


def get_new_brands2():
    opener = urllib.request.build_opener()
    url = 'http://www.jpx.co.jp/listing/stocks/new/index.html'
    html = opener.open(url).read()
    q = PyQuery(html.decode("utf-8"))
    for data in q.find("tbody > tr:even"):
        date = datetime.strptime(data[0].text, '%Y/%m/%d').date()
        code = data[2].find("span").get("id")
        name = data[1].find("a").text if len(data[1].findall("a")) > 0 else data[1].text.strip()
        yield (code, date, name)
