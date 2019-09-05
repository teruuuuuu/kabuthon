# -*- coding: utf-8 -*-
from simulation.order.order import Order


class BuyMarketOrderAsPossible(Order):
    """残高で買えるだけ買う成行注文
    """

    def __init__(self, code, unit):
        super().__init__(code)
        self.unit = unit

    def execute(self, date, portfolio, get_price_func):
        price = get_price_func(self.code, date)
        count_of_buying_unit = int(portfolio.deposit / price / self.unit)
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