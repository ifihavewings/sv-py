import time
from datetime import datetime
import os
from typing import Optional, List
import sys
from pathlib import Path

# 添加项目根目录到系统路径
project_root = str(Path(__file__).parent.parent.parent)
sys.path.append(project_root)

from app.players.AudioPlayer import AudioPlayer
from app.okx.PublicData import PublicAPI
from app.okx.config import InspectorConfig
from app.logger.ColorLogger import ColorLogger
from Strategy import Strategy

class PriceInspector:
    def __init__(self, config: InspectorConfig):
        """
        初始化价格监控器
        :param config: 监控器配置
        """
        self.config = config
        self.logger = ColorLogger
        self.audio_player = AudioPlayer()
        
        try:
            self.public_api = PublicAPI()
        except Exception as e:
            self.logger.error(f"初始化OKX API失败: {e}")
            raise

        if self.config.debug:
            self.logger.debug(f"初始化完成，配置信息: {self.config}")

    def play_alert(self):
        """播放报警声音"""
        try:
            self.audio_player.play_alert()
        except Exception as e:
            self.logger.error(f"播放报警声音失败: {e}")

    def check_conditions(self, klines: List) -> bool:
        """
        检查是否达到报警条件
        返回: 是否触发报警
        """
        straggies = Strategy(self.config, klines)
        should_alert = straggies.check_conditions()

        return should_alert

    def start_monitoring(self):
        """开始监控价格"""
        self.logger.info(f"开始监控 {self.config.symbol} 价格...")
        
        while True:
            try:
                # 获取K线数据
                klines = self.public_api.get_candlesticks(
                    instId=self.config.symbol,
                    bar=self.config.interval,
                    limit=self.config.limit
                )
                print(klines)
                if not klines:
                    self.logger.error("获取K线数据失败")
                    time.sleep(self.config.check_interval)
                    continue
                print(klines)
               
                
                if self.check_conditions(klines):
                    self.play_alert()
                    
                time.sleep(self.config.check_interval)
                
            except Exception as e:
                self.logger.error(f"监控出错: {e}")
                time.sleep(self.config.check_interval)
