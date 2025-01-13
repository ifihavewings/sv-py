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
"""
监控器:监控一个交易对的价格和涨跌幅, 基本使用方法是, 传入一个币种的名称, K线时间周期, K线数量, 目标价格, 目标涨幅, 检查间隔, 策略;
当价改币种的变化在指定的时间周期内达到预期的目标价格, 或者涨跌幅达到目标涨幅, 则播放报警声音
"""
class PriceInspector:
    def __init__(self, config: InspectorConfig):
        """
        初始化价格监控器
        :param config: 监控器配置
        """
        self.config = config
        self.logger = ColorLogger
        self.audio_player = AudioPlayer()
        self.klines = []
        
        try:
            self.public_api = PublicAPI()
        except Exception as e:
            self.logger.error(f"初始化OKX API失败: {e}")
            raise

        if self.config.debug:
            self.logger.debug(f"初始化完成，配置信息: {self.config}")

    def play_alert(self, opts):
        """播放报警声音"""
        try:
            self.audio_player.play(opts)
        except Exception as e:
            self.logger.error(f"播放报警声音失败: {e}")

    def check_conditions(self, klines: List) -> bool:
        """
        检查是否达到报警条件
        返回: 是否触发报警
        """
        strategy = Strategy(self.config, klines)
        check_result = strategy.check_conditions()

        if check_result['should_alert']:
            sound_type = None
            if check_result['change_type'] == 'up':
                sound_type = 'success'
            else:
                sound_type = 'failure'
            self.play_alert({'sound_type': sound_type})
            self.logger.success(f"{self.config.symbol} @ {self.klines[-1]['close']} # {round(check_result['change'], 2)}% ---> {self.klines}")

            return True
        else:   
            self.logger.info(f"{self.config.symbol} @ {self.klines[-1]['close']} # {round(check_result['change'], 2)}% ---> {self.klines}")
            return False
        

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
                
                if not klines:
                    self.logger.error("获取K线数据失败")
                    time.sleep(self.config.check_interval)
                    continue
               
                self.klines = klines
                self.check_conditions(klines)
                time.sleep(self.config.check_interval)
                
            except Exception as e:
                self.logger.error(f"监控出错: {e}")
                time.sleep(self.config.check_interval)
