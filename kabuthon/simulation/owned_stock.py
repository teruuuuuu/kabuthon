# -*- coding: utf-8 -*-
import math


class OwnedStock(object):
    def __init__(self):
        self.total_cost = 0  # 取得にかかったコスト（総額)
        self.total_count = 0  # 取得した株数(総数)
        self.current_count = 0  # 現在保有している株数
        self.average_cost = 0  # 平均取得価額

    def __str__(self):
        return f"OwnedStock(total_cost: {self.total_cost} total_count: {self.total_count} " + \
               f"current_cout: {self.current_count} avverage_cost: {self.average_cost})"

    def append(self, count, cost):
        if self.total_count != self.current_count:
            self.total_count = self.current_count
            self.total_cost = self.current_count * self.average_cost
        self.total_cost += cost
        self.total_count += count
        self.current_count += count
        self.average_cost = math.ceil(self.total_cost / self.total_count)

    def remove(self, count):
        if self.current_count < count:
            raise ValueError("can't remove", self.total_cost, count)
        self.current_count -= count
