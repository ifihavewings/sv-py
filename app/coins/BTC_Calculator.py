import requests
import time
import schedule
from decimal import Decimal, getcontext
from datetime import datetime

# 设置用于获取 BTC 价格的 API URL
url = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
# 设置用于获取 BTC Kline 数据的 API URL
kline_url = "https://api.binance.com/api/v3/klines"

# 设置 Decimal 的全局精度为小数点后四位
getcontext().prec = 4


class BTC_Calculator:
    def __init__(self):
        pass

    # 获取当前 BTC 价格
    def fetch_btc_price(self):
        try:
            response = requests.get(url)
            response.raise_for_status()  # 检查请求是否成功
            data = response.json()  # 获取返回的 JSON 数据
            price = data['price']  # 从返回的数据中提取价格
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

    # 获取 BTC 的 Kline 数据
    def fetch_btc_klines(self, opts):
        # 设置请求参数，包含交易对、时间间隔和数据条数
        params = {
            'symbol': opts['symbol'],
            'interval': '1' + opts['unit'],  # 根据单位选择时间间隔
            'limit': opts['limit']  # 获取最新指定数量的 Kline 数据
        }
        try:
            response = requests.get(kline_url, params=params)
            response.raise_for_status()  # 检查请求是否成功
            data = response.json()  # 获取返回的 JSON 数据
            if data:
                return data  # 如果数据存在，返回数据
            else:
                print("No data found.")  # 否则输出无数据
        except requests.exceptions.HTTPError as errh:
            print("Http Error:", errh)
        except requests.exceptions.ConnectionError as errc:
            print("Error Connecting:", errc)
        except requests.exceptions.Timeout as errt:
            print("Timeout Error:", errt)
        except requests.exceptions.RequestException as err:
            print("Something went wrong:", err)

    # 调度器每次调用的入口方法
    def run(self, opts):
        self.calculate(opts)  # 调用 calculate 方法进行计算

    '''
    Kline 数据格式：
    [
        1725667200000,       # 0 开盘时间（毫秒时间戳）
        '53962.97000000',    # 1 开盘价格（Open price）
        '54850.00000000',    # 2 最高价格（High price）
        '53745.54000000',    # 3 最低价格（Low price）
        '54160.86000000',    # 4 收盘价格（Close price）
        '16694.04774000',    # 5 成交量（Volume）
        1725753599999,       # 6 收盘时间（毫秒时间戳）
        '905693342.58983220',# 7 成交额（Quote asset volume）
        1920923,             # 8 成交笔数（Number of trades）
        '8023.90683000',     # 9 主动买入成交量（Taker buy base asset volume）
        '435381439.00959560',# 10 主动买入成交额（Taker buy quote asset volume）
        '0'                  # 11 未使用字段（Ignore）
    ]
    '''

    # 计算和显示 Kline 数据
    def calculate(self, opts):
        # 获取最新的 Kline 数据
        data = self.fetch_btc_klines(opts)
        if not data:
            return  # 如果没有数据，直接返回

        # 解析 Kline 数据
        kline = data[0]  # 获取最新的 Kline 数据
        open_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(kline[0] / 1000))
        moment = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(kline[6] / 1000))
        open_price = Decimal(kline[1])  # 开盘价
        high_price = Decimal(kline[2])  # 最高价
        low_price = Decimal(kline[3])  # 最低价
        close_price = Decimal(kline[4])  # 收盘价
        volume = Decimal(kline[5])  # 成交量
        quote_asset_volume = Decimal(kline[7])  # 成交额
        number_of_trades = Decimal(kline[8])  # 成交笔数
        taker_buy_base_asset_volume = Decimal(kline[9])  # 主动买入成交量
        taker_buy_quote_asset_volume = Decimal(kline[10])  # 主动买入成交额

        # 获取当前时间
        current_time = datetime.now()
        # 格式化为 "2024-09-12 07:59:59" 的形式
        formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")

        # 输出结果
        text = f"""
        {opts['symbol']} data: {opts['limit']} {opts['unit']}
        closeTime： {formatted_time}
        open： {open_price}
        close: {close_price}
        high： {high_price}
        low： {low_price}
        percentage：{(close_price - open_price) / open_price * 100:.2f}%
        Volume: {volume}
        quote_asset_volume: {quote_asset_volume}
        number_of_trades: {number_of_trades}
        taker_buy_base_asset_volume: {taker_buy_base_asset_volume}
        taker_buy_quote_asset_volume: {taker_buy_quote_asset_volume}
        """
        print(text)  # 打印计算结果
        self.append_to_file('./data.txt', text)
    # 将文本追加写入文件的函数
    def append_to_file(self, file_name, text):
        with open(file_name, 'a', encoding='utf-8') as file:  # 以追加模式打开文件
            file.write(text + '\n')  # 将文本写入文件，并换行


# 程序入口
if __name__ == "__main__":
    calculator = BTC_Calculator()

    # 每 5 秒调度一次计算 BTC 数据
    schedule.every(5).seconds.do(calculator.run, {
        'symbol': 'BTCUSDT',
        'limit': 1,
        'unit': 'd'
    })    # 每 5 秒调度一次计算 WLD 数据
    schedule.every(5).seconds.do(calculator.run, {
        'symbol': 'WLDUSDT',
        'limit': 1,
        'unit': 'd'
    })

    # 不断轮询执行调度任务
    while True:
        schedule.run_pending()  # 检查是否有任务需要执行
        time.sleep(1)  # 等待 1 秒以减少 CPU 占用
