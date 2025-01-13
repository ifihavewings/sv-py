from typing import Dict, Any
import requests
from PublicData import PublicAPI

from config import InspectorConfig
from Inspector import PriceInspector


# 测试 public api

# try:
#     api = PublicAPI()
#     trading_pair = "BTC-USDT"  # 交易对
#     bar_interval = "5m"        # 时间周期
#     data_limit = 1            # K 线数量

#     # 获取 K 线数据
#     candlestick_data: Dict[str, Any] = api.get_candlesticks(
#         instId=trading_pair,
#         bar=bar_interval,
#         limit=data_limit
#     )

#     # 输出结果
#     print("K 线数据：")
#     print(candlestick_data)

# except Exception as e:
#     print(f"发生错误：{str(e)}")

# 测试 inspector
try:
    print(1)
    config = InspectorConfig(symbol="BTC-USDT", interval="5m", target_price=100000, target_change=3, check_interval=30, limit=1, strategy="price")
    inspector = PriceInspector(config)
    inspector.start_monitoring()
    print(2)
except Exception as e:
    print(3)
    print(f"发生错误：{str(e)}")
