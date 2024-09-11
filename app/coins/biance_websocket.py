import asyncio
import websockets


async def binance_websocket():
    url = "wss://stream.binance.com:9443/ws/btcusdt@trade"

    try:
        async with websockets.connect(url) as websocket:
            while True:
                response = await websocket.recv()
                print(response)
    except (websockets.exceptions.ConnectionClosedError, asyncio.TimeoutError) as e:
        print(f"Connection error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


# 使用 asyncio.run() 来启动事件循环
asyncio.run(binance_websocket())
