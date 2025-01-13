import requests
from typing import Dict, Any, Optional, List
from datetime import datetime
class PublicAPI:
    """OKX 公共 API 接口封装"""
    
    BASE_URL = "https://www.okx.com"
    
    def __init__(self):
        """初始化 PublicAPI"""
        self.session = requests.Session()
        # 设置请求头
        self.session.headers.update({
            "Accept": "application/json",
            "Content-Type": "application/json",
            "User-Agent": "OKX-Price-Inspector"
        })

    def _request(self, method: str, path: str, **kwargs) -> Dict[str, Any]:
        """
        发送 HTTP 请求到 OKX API
        
        :param method: HTTP 方法 (GET, POST 等)
        :param path: API 路径
        :param kwargs: 请求参数
        :return: API 响应数据
        """
        url = f"{self.BASE_URL}{path}"
        try:
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"API 请求失败: {str(e)}")

    def get_candlesticks(self, instId: str, bar: str = "5m", limit: int = 1) -> Dict[str, Any]:
        """
        获取K线数据
        
        :param instId: 交易对，例如 "BTC-USDT"
        :param bar: K线周期，默认1分钟："1m", "3m", "5m", "15m", "30m", "1H", "2H", "4H"
        :param limit: 获取条数，默认1条
        :return: K线数据
        """
        path = "/api/v5/market/candles"
        params = {
            "instId": instId,
            "bar": bar,
            "limit": str(limit)
        }
        try:    
            data = self._request("GET", path, params=params)
            if data.get("code") == "0":
                return self.format_candlesticks(data.get("data"))
            else:
                print(f"API 请求失败: {data.get('msg')}")
                return []
        except Exception as e:
            print(f"发生错误：{str(e)}")
            return []
    def format_candlesticks(self, candlesticks: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        格式化 K 线数据
        """
        return [{"timestamp": self.convert_timestamp_to_datetime(item[0]), "open": item[1], "high": item[2], "low": item[3], "close": item[4], "volume": item[5], "turnover": item[6], "leverage_turnover": item[7]} for item in candlesticks]

    from datetime import datetime

    def convert_timestamp_to_datetime(self,timestamp):
        timestamp_seconds = int(timestamp) / 1000
        dt_object = datetime.fromtimestamp(timestamp_seconds)
        return dt_object.strftime('%Y-%m-%d %H:%M:%S')

