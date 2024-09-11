from coins.WebElementWatcher import WebElementWatcher


if __name__ == '__main__':
    watcher = WebElementWatcher('https://www.binance.com/zh-CN/futures/BTCUSDT', interval=5)
    watcher.start_watching()