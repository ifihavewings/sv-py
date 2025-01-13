from config import InspectorConfig
from typing import List
class Strategy:
    def __init__(self, config: InspectorConfig, klines: List):
        self.config = config
        self.klines = klines

    def check_conditions(self) -> bool:

        should_alert = False
        change_type = None

        if "BTC" in self.config.symbol:
            print("BTC-USDT")
        else:
            if self.config.strategy == "price":
                should_alert =  False

            elif self.config.strategy == "change":
                latest_kline = self.klines[-1]
                
                # 计算涨幅
                change = (float(latest_kline['close']) - float(latest_kline['open'])) / float(latest_kline['open']) * 100
                change_abs = abs(change)
                if change_abs >= self.config.target_change:
                    should_alert =  True
                    if change > 0:  
                        change_type = 'up'
                    else:
                        change_type = 'down'
                else:
                    should_alert =  False
            return {'should_alert': should_alert, 'change_type': change_type, 'change': change}

