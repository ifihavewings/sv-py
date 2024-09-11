import requests
from bs4 import BeautifulSoup
import time
import schedule


class WebElementWatcher:
    def __init__(self, url, parse_function=None, interval=10):
        self.url = url
        self.interval = interval  # 轮询的间隔时间，单位是秒
        self.last_value = None  # 存储上次的解析结果
        self.parse_function = parse_function or self.default_parse_function

    def default_parse_function(self, html):
        """
        默认的页面解析函数，可以根据需要修改。
        例如，获取 BTC/USDT 期货价格。
        """
        soup = BeautifulSoup(html, 'html.parser')
        # 这个选择器需要根据页面结构自行调整
        price_element = soup.find('div', {'class': 'some-class-for-price'})
        if price_element:
            return price_element.text.strip()
        return None

    def fetch_page(self):
        """
        获取页面 HTML 内容。
        """
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"Error fetching the page: {e}")
            return None

    def watch(self):
        """
        核心方法，负责获取页面并解析变化。
        """
        html = self.fetch_page()
        if html:
            current_value = self.parse_function(html)
            if current_value and current_value != self.last_value:
                print(f"Element changed: {self.last_value} -> {current_value}")
                self.last_value = current_value
            else:
                print("No change detected.")
        else:
            print("Failed to fetch or parse the page.")

    def start_watching(self):
        """
        启动轮询监听，使用 schedule 库进行定时调用。
        """
        schedule.every(self.interval).seconds.do(self.watch)
        while True:
            schedule.run_pending()
            time.sleep(1)


# 自定义的页面解析函数
def custom_parse_function(html):
    soup = BeautifulSoup(html, 'html.parser')
    # 例如，解析某个特定的元素
    price_element = soup.find('span', {'class': 'price-tag'})  # 自定义解析规则
    if price_element:
        return price_element.text.strip()
    return None


# 示例用法
if __name__ == "__main__":
    print(111)

    url = 'https://www.binance.com/zh-CN/futures/BTCUSDT'

    # 使用默认解析函数
    watcher = WebElementWatcher(url, interval=5)
    watcher.start_watching()

    # 使用自定义解析函数
    # watcher = WebElementWatcher(url, parse_function=custom_parse_function, interval=30)
    # watcher.start_watching()
