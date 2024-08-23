import websocket
import json
import queue
import threading
from datetime import datetime
from collections import defaultdict
import time

trade_queue = queue.Queue()

minute_trades = defaultdict(list)

def on_message(ws, message):
    trade_data = json.loads(message)
    if trade_data['type'] == 'trade':
        for trade in trade_data['data']:
            symbol = trade['s']
            price = trade['p']
            volume = trade['v']
            timestamp = trade['t']
            
            trade_time = datetime.fromtimestamp(timestamp / 1000)
            trade_minute = trade_time.strftime('%Y-%m-%d %H:%M')
            
            minute_trades[(symbol, trade_minute)].append((price, volume, trade_time))

            write_trade_to_file(symbol, price, volume, timestamp)

def write_trade_to_file(symbol, price, volume, timestamp):
    filename = f"{symbol}_trades.txt"
    with open(filename, 'a') as f:
        f.write(f"{timestamp},{price},{volume}\n")

def on_error(ws, error):
    print("An error occurred:")
    print(error)

def on_close(ws):
    print("WebSocket connection closed.")

def on_open(ws):
    print("WebSocket connection opened.")
    ws.send('{"type":"subscribe","symbol":"AAPL"}')
    ws.send('{"type":"subscribe","symbol":"AMZN"}')
    ws.send('{"type":"subscribe","symbol":"BINANCE:BTCUSDT"}')

def calculate_and_log_candlestick(symbol, trade_minute, trades):
    if not trades:
        return
    
    open_price = trades[0][0]
    high_price = max(trades, key=lambda x: x[0])[0]
    low_price = min(trades, key=lambda x: x[0])[0]
    close_price = trades[-1][0]
    total_volume = sum(trade[1] for trade in trades)
    
    filename = f"{symbol}_candlesticks.txt"
    with open(filename, 'a') as f:
        f.write(f"{trade_minute},{open_price},{high_price},{low_price},{close_price},{total_volume}\n")
    print(f"Logged candlestick for {symbol} at {trade_minute}")

def process_minute_candlesticks():
    while True:
        now = datetime.now()
        current_minute = now.strftime('%Y-%m-%d %H:%M')
        
        for (symbol, trade_minute), trades in list(minute_trades.items()):
            if trade_minute != current_minute:
                calculate_and_log_candlestick(symbol, trade_minute, trades)
                del minute_trades[(symbol, trade_minute)]
        

def calculate_and_log_moving_average(symbol):
    with open(f"{symbol}_candlesticks.txt", 'r') as f:
        lines = f.readlines()[-15:]  # Get the last 15 lines
    
    if len(lines) < 15:
        return  # Not enough data yet
    
    prices = []
    volumes = []
    for line in lines:
        parts = line.strip().split(',')
        close_price = float(parts[4])
        volume = float(parts[5])
        prices.append(close_price)
        volumes.append(volume)
    
    price_moving_avg = sum(prices) / len(prices)
    volume_moving_avg = sum(volumes) / len(volumes)
    
    with open(f"{symbol}_moving_avg.txt", 'a') as f:
        f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M')},{price_moving_avg},{volume_moving_avg}\n")
    print(f"Logged moving average for {symbol}")

def process_moving_averages():
    while True:
        for symbol, _ in minute_trades.keys():
            calculate_and_log_moving_average(symbol)
        time.sleep(60)  # Calculate every minute


API_KEY = 'cqh7jvhr01qm46d7cio0cqh7jvhr01qm46d7ciog'

websocket_url = f"wss://ws.finnhub.io?token={API_KEY}"

ws = websocket.WebSocketApp(
    websocket_url,
    on_message=on_message,  # Callback function to handle incoming messages
    on_error=on_error,      # Callback function to handle errors
    on_close=on_close       # Callback function to handle the closing of the connection
)

ws.on_open = on_open

threading.Thread(target=process_minute_candlesticks, daemon=True).start()

threading.Thread(target=process_moving_averages, daemon=True).start()

ws.run_forever()


import pandas as pd

aapl_trades = pd.read_csv('AAPL_trades.txt', header=None, names=['timestamp', 'price', 'volume'])
print(aapl_trades.head())

import pandas as pd

aapl_trades = pd.read_csv('AAPL_trades.txt', header=None, names=['timestamp', 'price', 'volume'])
aapl_candlesticks = pd.read_csv('AAPL_candlesticks.txt', header=None, names=['minute', 'open', 'high', 'low', 'close', 'volume'])


aapl_trades['timestamp'] = pd.to_datetime(aapl_trades['timestamp'], unit='ms')


import matplotlib.pyplot as plt

cpu_idle_times = pd.read_csv('cpu_idle_times.txt', header=None, names=['idle_time'])

plt.plot(cpu_idle_times['idle_time'])
plt.xlabel('Time (minutes)')
plt.ylabel('CPU Idle Time (%)')
plt.title('CPU Idle Time Over Execution')
plt.show()

