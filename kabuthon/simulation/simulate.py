# -*- coding: utf-8 -*-
import os

import pandas as pd
import slack

from db.repository.brand_repo import BrandRepo
from simulation.order.buy_market_order_as_possible import BuyMarketOrderAsPossible
from simulation.order.sell_market_order import SellMarketOrder
from simulation.portfolio import Portfolio
from datetime import datetime
import matplotlib.pyplot as plt


def tse_date_range(start_date, end_date):
    tse_business_day = pd.offsets.CustomBusinessDay()
    return pd.date_range(start_date, end_date,
                         freq=tse_business_day)


def generate_cross_date_list(prices):
    """指定した日足データよりゴールデンクロス・デッドクロスが生じた日のリストを生成
    """
    # 移動平均を求める
    sma_5 = prices.rolling(window=5).mean()
    sma_25 = prices.rolling(window=25).mean()

    # ゴールデンクロス・デッドクロスが発生した場所を得る
    sma_5_over_25 = sma_5 > sma_25
    cross = sma_5_over_25 != sma_5_over_25.shift(1)
    golden_cross = cross & (sma_5_over_25 is True)
    dead_cross = cross & (sma_5_over_25 is False)
    golden_cross.drop(golden_cross.head(25).index, inplace=True)
    dead_cross.drop(dead_cross.head(25).index, inplace=True)

    # 日付のリストに変換
    golden_list = [x.date()
                   for x
                   in golden_cross[golden_cross].index.to_pydatetime()]
    dead_list = [x.date()
                 for x
                 in dead_cross[dead_cross].index.to_pydatetime()]
    return golden_list, dead_list


def simulate():
    def make_price_df(brands):
        df = pd.DataFrame(columns=['code', 'date', 'open', 'high', 'low', 'close',
                                   'golden_cross', 'dead_cross']).set_index(['code', 'date'])
        for brand in brands:
            code = brand.code
            prices = BrandRepo().select_prices(code)
            data = {'code': list(map(lambda p: p.code, prices)),
                    'date': list(map(lambda p: p.date, prices)),
                    'open': list(map(lambda p: p.open, prices)),
                    'high': list(map(lambda p: p.high, prices)),
                    'low': list(map(lambda p: p.low, prices)),
                    'close': list(map(lambda p: p.close, prices))}
            brand_df = pd.DataFrame(data).set_index(['code', 'date'])
            sma_5 = brand_df.groupby(level='code')['close'].rolling(window=5).mean()
            sma_25 = brand_df.groupby(level='code')['close'].rolling(window=25).mean()
            sma_5_over_25 = sma_5 > sma_25
            cross = sma_5_over_25 != sma_5_over_25.shift(1)
            golden_cross = cross & (sma_5_over_25 == True)
            dead_cross = cross & (sma_5_over_25 == False)
            brand_df['sma_5'] = brand_df.groupby(level='code')['close'].rolling(window=5).mean().values
            brand_df['sma_25'] = brand_df.groupby(level='code')['close'].rolling(window=25).mean().values
            brand_df['sma_5_over_25'] = sma_5_over_25.values
            brand_df['golden_cross'] = golden_cross.values
            brand_df['dead_cross'] = dead_cross.values
            df = df.append(brand_df[25:], sort=True)
        return df

    def trade_func(brands, date, portfolio):
        orders = []
        # Dead crossが発生していて持っている株があれば売る
        for brand in brands:
            code = brand.code
            if date in price_df.loc[code].index and price_df.loc[code, date].dead_cross \
                    and code in portfolio.stocks:
                print("sell")
                orders.append(SellMarketOrder(code, portfolio.stocks[code].current_count))
        # 保有していない株でgolden crossが発生していたら買う
        if brand in brands:
            code = brand.code
            unit = brand.unit
            if date in price_df.loc[code].index and price_df.loc[code, date].golden_cross \
                    and code not in portfolio.stocks:
                print("buy")
                orders.append(BuyMarketOrderAsPossible(code, unit))
        return orders

    def get_open_price_func(code, date):
        return price_df.loc[code, date].open

    def get_close_price_func(code, date):
        return price_df.loc[code, date].close

    def current_price(d):
        # 本日(d)の損益などを記録
        current_total_price = portfolio.calc_current_total_price(
            lambda code, date: get_close_price_func(code, date), d)
        return current_total_price, current_total_price - portfolio.amount_of_investment
        total_price_list.append(current_total_price)
        profit_or_loss_list.append(current_total_price - portfolio.amount_of_investment)

    def simulate(portfolio, df):
        def execute_order(d, orders):
            # 本日(d)において注文(orders)をすべて執行する
            for order in orders:
                executions.append(order.execute(d, portfolio, get_open_price_func))

        orders = []
        total_price_list = []
        profit_or_loss_list = []
        executions = []
        for current_date in date_range:
            # シミュレーション
            execute_order(current_date, orders)
            total_price, profit_or_loss = current_price(current_date)
            total_price_list.append(total_price)
            profit_or_loss_list.append(profit_or_loss)
            orders = trade_func(brand_list, current_date, portfolio)
        return total_price_list, profit_or_loss_list, executions

    portfolio = Portfolio(10000000)
    brand_list = list(BrandRepo().select_all_brand())
    price_df = make_price_df(brand_list)
    date_range = [pdate.to_pydatetime().date()
                  for pdate in tse_date_range(
            price_df.sort_values(by='date', ascending=True).head(1).index.get_level_values('date')[0],
            price_df.sort_values(by='date', ascending=False).head(1).index.get_level_values('date')[0])]
    total_price_list, profit_or_loss_list, executions = simulate(portfolio, price_df)

    profit_df = pd.DataFrame({'date': date_range,
                              'profit_or_loss': profit_or_loss_list}).set_index('date')
    save_dataframe(profit_df, 'temp/simulate.png')

    execution_str = ""
    for execution in executions:
        execution_str += str(execution) + "\n"
    slack_comment(execution_str)
    slack_file_upload('temp/simulate.png')


def save_dataframe(df, image_name):
    plt.figure()
    df.plot()
    plt.savefig(image_name)
    plt.close('all')


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