# -*- coding: utf-8 -*-
import time

import notification.brand as brand
from mpl_finance import candlestick2_ohlc, volume_overlay

def brand_notification():
    print("notification start")
    brand.new_brand_notification()
    brand.brand_notification()
    brand.price_notification()
    print("notification end")