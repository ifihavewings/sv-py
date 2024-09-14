from BTC_Calculator import BTC_Calculator
import schedule
import time
class PriceWarning:


    def __init__(self):
        pass

    def run(self):
        calculator = BTC_Calculator()

        # 每 5 秒调度一次计算 BTC 数据
        schedule.every(5).seconds.do(calculator.run, {
            'symbol': 'BTCUSDT',
            'limit': 1,
            'unit': 'd',
            'warning': True
        })  # 每 5 秒调度一次计算 WLD 数据
        schedule.every(5).seconds.do(calculator.run, {
            'symbol': 'WLDUSDT',
            'limit': 1,
            'unit': 'd',
            'warning': True
        })

        # 不断轮询执行调度任务
        while True:
            schedule.run_pending()  # 检查是否有任务需要执行
            time.sleep(1)  # 等待 1 秒以减少 CPU 占用
