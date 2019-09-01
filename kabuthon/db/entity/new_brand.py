# -*- coding: utf-8 -*-
from datetime import datetime


class NewBrand:
    code = None
    date = None
    name = None

    def __init__(self, code, date, name):
        assert type(code) is str, 'code is str'
        assert code.strip() is not '', 'code needs input'
        assert type(date) is str, 'date is str'
        assert date.strip() is not '', 'date needs input'
        assert type(name) is str, 'name is str'
        self.code = code
        self.date = datetime.strptime(date, "%Y/%m/%d")
        self.name = name

    def format_date(self):
        return self.date.strftime('%Y/%m/%d')
