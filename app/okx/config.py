from dataclasses import dataclass
from typing import Optional, Literal
import os

@dataclass
class InspectorConfig:
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
