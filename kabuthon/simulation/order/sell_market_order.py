# -*- coding: utf-8 -*-
from simulation.order.order import Order


class SellMarketOrder(Order):
    """成行の売り注文
    """
    def __init__(self, code, count):
        super().__init__(code)
        self.count = count

    def execute(self, date, portfolio, get_price_func):
        price = get_price_func(self.code, date)
        prev_deposit = portfolio.deposit
        portfolio.sell_stock(self.code, self.count, price)
        self.logger("SELL", date, self.code, self.count, price, prev_deposit, portfolio.deposit)
        return "SELL", date, self.code, self.count, price, prev_deposit, portfolio.deposit