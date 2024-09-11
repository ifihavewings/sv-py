import requests
from bs4 import BeautifulSoup
import time
import schedule
from decimal import Decimal, getcontext
from datetime import datetime

url = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
kline_url = "https://api.binance.com/api/v3/klines"
# 设置精度为小数点后两位
getcontext().prec = 4
class BTC_Calculator:
    def __init__(self):
       pass

    def fetch_btc_price(self):
       try:
           response = requests.get(url)
           response.raise_for_status()
           data = response.json()
           price = data['price']
           print(f"BTC Price: {price}")
           return data
       except requests.exceptions.HTTPError as errh:
           print("Http Error:", errh)
       except requests.exceptions.ConnectionError as errc:
           print("Error Connecting:", errc)
       except requests.exceptions.Timeout as errt:
           print("Timeout Error:", errt)
       except requests.exceptions.RequestException as err:
           print("Something went wrong:", err)


    def fetch_btc_klines(self, opts):

        params = {
            'symbol': 'BTCUSDT',
            'interval': '1'+ opts['unit'],
            'limit': opts['limit']  # 获取最新一天的 Kline 数据
        }

        try:
            response = requests.get(kline_url, params=params)
            response.raise_for_status()
            data = response.json()

            # 提取 Kline 数据
            if data:
                return data
            else:
                print("No data found.")

        except requests.exceptions.HTTPError as errh:
            print("Http Error:", errh)
        except requests.exceptions.ConnectionError as errc:
            print("Error Connecting:", errc)
        except requests.exceptions.Timeout as errt:
            print("Timeout Error:", errt)
        except requests.exceptions.RequestException as err:
            print("Something went wrong:", err)

    def run(self, opts):
        while True:
            self.calculate(opts)
            time.sleep(5)

    '''
    calculate_options: {
        'interval': 1d | 5d | 10d | 20d | 1M | 2M | 3M | 4M | 5M | 6M | 7M | 8M | 9M
    }
    data: 
    [
        1725667200000,       # 0 开盘时间（毫秒时间戳）
        '53962.97000000',    # 1 开盘价格（Open price）
        '54850.00000000',    # 2 最高价格（High price）
        '53745.54000000',    # 3 最低价格（Low price）
        '54160.86000000',    # 4 收盘价格（Close price）
        '16694.04774000',    # 5 成交量（Volume）
        1725753599999,       # 6 收盘时间（毫秒时间戳）
        '905693342.58983220',# 7 成交额（Quote asset volume，成交额，单位是 quote 货币，即 BTCUSDT 中的 USDT）
        1920923,             # 8 成交笔数（Number of trades）
        '8023.90683000',     # 9 主动买入成交量（Taker buy base asset volume，主动买单的成交量）
        '435381439.00959560',# 10 主动买入成交额（Taker buy quote asset volume，主动买单的成交额）
        '0'                  # 11 未使用字段（Ignore）
    ]

    '''

    def calculate(self, opts):
        data = self.fetch_btc_klines(opts)
        kline = data[0]  # 获取最新的 Kline 数据
        open_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(kline[0] / 1000))
        moment = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(kline[6] / 1000))
        open_price = Decimal(kline[1])
        high_price = Decimal(kline[2])
        low_price = Decimal(kline[3])
        close_price = Decimal(kline[4])
        volume = Decimal(kline[5])
        quote_asset_volume = Decimal(kline[7])
        number_of_trades = Decimal(kline[8])
        taker_buy_base_asset_volume = Decimal(kline[9])
        taker_buy_quote_asset_volume = Decimal(kline[10])
        # 获取当前时间
        current_time = datetime.now()
        # 格式化为 "2024-09-12 07:59:59" 的形式
        formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
        text = f"""
        BTC data: {opts['limit']} {opts['unit']}
        closeTime： {current_time}
        open： {open_price}
        close: {close_price}
        high： {high_price}
        low： {low_price}
        percentage：{ (close_price - open_price) / open_price * 100 }%
        Volume: {volume}
        quote_asset_volume: {quote_asset_volume}
        number_of_trades: {number_of_trades}
        taker_buy_base_asset_volume: {taker_buy_base_asset_volume}
        taker_buy_quote_asset_volume: {taker_buy_quote_asset_volume}
        """
        print(text)





if __name__ == "__main__":
    calculator = BTC_Calculator()
    calculator.run({
        'limit': 1,
        'unit': 'd'
    });