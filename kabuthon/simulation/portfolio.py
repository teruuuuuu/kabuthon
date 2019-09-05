# -*- coding: utf-8 -*-
import collections
from functools import reduce

from simulation.owned_stock import OwnedStock


def calc_fee(total):
    """約定手数料計算(楽天証券の場合）
    """
    if total <= 50000:
        return 54
    elif total <= 100000:
        return 97
    elif total <= 200000:
        return 113
    elif total <= 500000:
        return 270
    elif total <= 1000000:
        return 525
    elif total <= 1500000:
        return 628
    elif total <= 30000000:
        return 994
    else:
        return 1050


def calc_cost_of_buying(count, price):
    """株を買うのに必要なコストと手数料を計算
    """
    subtotal = int(count * price)
    fee = calc_fee(subtotal)
    return subtotal + fee, fee


def calc_cost_of_selling(count, price):
    """株を売るのに必要なコストと手数料を計算
    """
    subtotal = int(count * price)
    fee = calc_fee(subtotal)
    return fee, fee


def calc_tax(total_profit):
    """儲けに対する税金計算
    """
    if total_profit < 0:
        return 0
    return int(total_profit * 0.20315)


class Portfolio(object):

    def __init__(self, deposit):
        self.deposit = deposit  # 現在の預り金
        self.amount_of_investment = deposit  # 投資総額
        self.total_profit = 0  # 総利益（税引き前）
        self.total_tax = 0  # （源泉徴収)税金合計
        self.total_fee = 0  # 手数料合計
        self.stocks = collections.defaultdict(OwnedStock)  # 保有銘柄 銘柄コード　-> OwnedStock への辞書

    def __str__(self):
        def stocks_str():
            ret = "["
            for stock in self.stocks.values():
                ret += str(stock)
            ret += "]"
            return ret
        return f"""口座情報表示
　現在の預り金: {self.deposit}
　投資総額: {self.amount_of_investment}
　総利益(税引前): {self.total_profit}
　(源泉徴収)税金合計: {self.total_tax}
　手数料合計: {self.total_fee}
　保有銘柄: {stocks_str()}"""

    def add_deposit(self, deposit):
        """預り金を増やす (= 証券会社に入金)
        """
        self.deposit += deposit
        self.amount_of_investment += deposit

    def buy_stock(self, code, count, price):
        """株を買う
        """
        cost, fee = calc_cost_of_buying(count, price)
        if cost > self.deposit:
            raise ValueError('cost > deposit', cost, self.deposit)

        # 保有株数増加
        self.stocks[code].append(count, cost)

        self.deposit -= cost
        self.total_fee += fee

    def sell_stock(self, code, count, price):
        """株を売る
        """
        subtotal = int(count * price)
        cost, fee = calc_cost_of_selling(count, price)
        if cost > self.deposit + subtotal:
            raise ValueError('cost > deposit + subtotal',
                             cost, self.deposit + subtotal)

        # 保有株数減算
        stock = self.stocks[code]
        average_cost = stock.average_cost
        stock.remove(count)
        if stock.current_count == 0:
            del self.stocks[code]

        # 儲け計算
        profit = int((price - average_cost) * count - cost)
        self.total_profit += profit

        # 源泉徴収額決定
        current_tax = calc_tax(self.total_profit)
        withholding = current_tax - self.total_tax
        self.total_tax = current_tax

        self.deposit += subtotal - cost - withholding
        self.total_fee += fee

    def calc_current_total_price(self, get_current_price_func, date):
        """現在の評価額を返す
        """
        stock_price = sum(get_current_price_func(code, date)
                          * stock.current_count
                          for code, stock in self.stocks.items())
        return stock_price + self.deposit
