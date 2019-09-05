# -*- coding: utf-8 -*-
import os
import time

import pandas as pd
from pandas.plotting import register_matplotlib_converters
import matplotlib.pyplot as plt
import numpy as np
import slack
from matplotlib.dates import date2num
from mpl_finance import candlestick_ohlc

from db.repository.brand_repo import BrandRepo


def save_dataframe(df, image_name):
    fig, ax = plt.subplots(figsize=(len(df.columns) * 2, df.size / 2))
    ax.axis('off')
    ax.axis('tight')
    ax.table(cellText=df.values,
             colLabels=df.columns,
             loc='center',
             bbox=[0, 0, 1, 1])
    plt.savefig(image_name)

def slack_file_upload(file_path):
    client = slack.WebClient(token=os.environ['SLACK_API_TOKEN'])
    response = client.files_upload(
        channels=os.environ['SLACK_CHANNEL'],
        file=file_path)
    assert response["ok"]

def slack_comment(comment):
    client = slack.WebClient(token=os.environ['SLACK_API_TOKEN'])
    response = client.chat_postMessage(
        channel=os.environ['SLACK_CHANNEL'],
        text=comment)
    assert response["ok"]
    assert response["message"]["text"] == comment

def new_brand_notification():
    df = pd.DataFrame(list(map(lambda new_brand: (new_brand.code, new_brand.format_date(), new_brand.name),
                               BrandRepo().select_new_brand_recently()))
                      , columns=["code", "date", "name"])
    slack_comment("新株情報\n" + str(df))

def brand_notification():
    df = pd.DataFrame(list(map(lambda brand: (brand.code, brand.name, brand.short_name,
                                              brand.market, brand.sector, brand.unit),
                               BrandRepo().select_all_brand()))
                      , columns=["code", "name", "short_name", "market", "sector", "unit"])
    slack_comment("監視対象株\n" + str(df))

def price_notification():
    # TODO 監視対象企業が30社の場合に描画している図が多いという警告が出たのでなおす
    #  RuntimeWarning: More than 20 figures have been opened. Figures created through the pyplot interface (`matplotlib.pyplot.figure`
    # ) are retained until explicitly closed and may consume too much memory. (To control this warning, see the rcParam `figure.max_open_warning`).
    #   fig = plt.figure()
    for brand in BrandRepo().select_all_brand():
        code = brand.code
        name = brand.name
        file_path = f'temp/{code}_candle.png'
        prices = BrandRepo().select_prices(code)
        data = {'date': list(map(lambda p: p.date, prices)),
                'open': list(map(lambda p: p.open, prices)),
                'high': list(map(lambda p: p.high, prices)),
                'low': list(map(lambda p: p.low, prices)),
                'close': list(map(lambda p: p.close, prices))}
        df = pd.DataFrame(data).set_index("date")
        fig = plt.figure()
        ax = plt.subplot()

        xdate = [x.date() for x in df.index]  # Timestamp -> datetime
        ohlc = np.vstack((date2num(xdate), df.values.T)).T  # datetime -> float
        candlestick_ohlc(ax, ohlc, width=0.7, colorup='g', colordown='r')
        ax.grid()  # グリッド表示
        register_matplotlib_converters()
        ax.set_xlim(df.index[0].date(), df.index[-1].date())  # x軸の範囲
        fig.autofmt_xdate()  # x軸のオートフォーマット
        plt.savefig(file_path)
        slack_comment(f'{code} {name} ローソク足チャート')
        time.sleep(10)
        slack_file_upload(file_path)
        time.sleep(10)
        os.remove(file_path)
