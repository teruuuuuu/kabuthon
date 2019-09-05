# -*- coding: utf-8 -*-
from simulation.order.order import Order


class BuyMarketOrderMoreThan(Order):
    """指定額以上で最小の株数を買う
    """
    def __init__(self, code, unit, under_limit):
        super().__init__(code)
        self.unit = unit
        self.under_limit = under_limit

    def execute(self, date, portfolio, get_price_func):
        price = get_price_func(self.code, date)
        unit_price = price * self.unit
        if unit_price > self.under_limit:
            count_of_buying_unit = 1
        else:
            count_of_buying_unit = int(self.under_limit / unit_price)
        while count_of_buying_unit:
            try:
                count = count_of_buying_unit * self.unit
                prev_deposit = portfolio.deposit
                portfolio.buy_stock(self.code, count, price)
                self.logger("BUY", date, self.code, count, price, prev_deposit, portfolio.deposit)
                return "BUY", date, self.code, count, price, prev_deposit, portfolio.deposit
            except ValueError:
                count_of_buying_unit -= 1
            else:
                break