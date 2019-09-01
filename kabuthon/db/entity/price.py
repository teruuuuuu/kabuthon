# -*- coding: utf-8 -*-
from datetime import datetime


class Price:
    code = None
    date = None
    open = None
    high = None
    low = None
    close = None
    volume = None
    adjust_close = None

    def __init__(self, code, date, open, high, low, close, volume, adjust_close):
        assert type(code) is str, 'code is str'
        assert code.strip() is not '', 'code needs input'
        assert type(date) is datetime, 'date is datetime.datetime'
        assert type(open) is float, 'open is float'
        assert type(high) is float, 'high is float'
        assert type(low) is float, 'low is float'
        assert type(close) is float, 'close is float'
        assert type(volume) is int, 'volume is int'
        assert type(adjust_close) is float, 'adjust_close is float'
        self.code = code.strip()
        self.date = date
        self.open = open
        self.high = high
        self.low = low
        self.close = close
        self.volume = volume
        self.adjust_close = adjust_close

    def __str__(self):
        return f"Price({self.code}, {self.format_date()}, {self.open}, {self.high}, {self.low}, {self.close}, {self.volume}, {self.adjust_close})"

    def format_date(self):
        return self.date.strftime('%Y/%m/%d')