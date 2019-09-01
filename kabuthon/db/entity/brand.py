# -*- coding: utf-8 -*-


class Brand:
    code = None
    name = None
    short_name = None
    market = None
    sector = None
    unit = None

    def __init__(self, code, name, short_name, market, sector, unit):
        assert code.strip() is not ''
        assert name.strip() is not ''
        assert short_name.strip() is not ''
        assert market.strip() is not ''
        assert sector.strip() is not ''
        assert unit is not 0
        self.code = code
        self.name = name
        self.short_name = short_name
        self.market = market
        self.sector = sector
        self.unit = unit