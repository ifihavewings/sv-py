from dataclasses import dataclass
from typing import Optional, Literal
import os

@dataclass
class InspectorConfig:
    """
    监控配置
    symbol: 交易对
    interval: K线时间周期, 例如: 1m, 5m, 15m, 30m, 1h, 4h, 1d
    target_price: 目标价格
    target_change: 目标涨幅
    check_interval: 检查间隔, 单位秒
    limit: K线数量
    strategy: 策略
    debug: 是否开启调试
    """
    symbol: str
    interval: str
    target_price: Optional[float] = None
    target_change: Optional[float] = None
    check_interval: int = 60
    limit: int = 1
    strategy: Literal["price", "change"] = "price"
    debug: bool = False

    def __post_init__(self):
        if not self.target_price and not self.target_change:
            raise ValueError("必须设置 target_price 或 target_change 中的至少一个")
        
        # if not os.path.exists(self.api_key_path):
        #     raise FileNotFoundError(f"API配置文件不存在: {self.api_key_path}")
