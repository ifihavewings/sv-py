from config import InspectorConfig
from typing import List
class Strategy:
    def __init__(self, config: InspectorConfig, klines: List):
        self.config = config
        self.klines = klines

    def check_conditions(self) -> bool:

        should_alert = False
        print(self.config)
        if self.config.strategy == "price":
            print('change')
            print(self.klines)
            print(self.config)

            return False
        elif self.config.strategy == "change":
            print('change')
            print(self.klines)
            print(self.config)
            # 计算涨幅
            """
            如果监测的是1分钟K线，则涨幅为1个点就报警
            如果监测的是5分钟K线，则涨幅为2个点就报警
            如果监测的是15分钟K线，则涨幅为4个点就报警
            """
            return False
        return False
