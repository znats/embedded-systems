# analysis.py

import pandas as pd
import matplotlib.pyplot as plt

# Load trades data
aapl_trades = pd.read_csv('AAPL_trades.txt', header=None, names=['timestamp', 'price', 'volume'])
print("AAPL Trades Data:")
print(aapl_trades.head())

# Load the trades and candlestick data
aapl_trades = pd.read_csv('AAPL_trades.txt', header=None, names=['timestamp', 'price', 'volume'])
aapl_candlesticks = pd.read_csv('AAPL_candlesticks.txt', header=None, names=['minute', 'open', 'high', 'low', 'close', 'volume'])

# Example of calculating the time difference for analysis
# Assuming timestamp is in milliseconds and converting it to datetime
aapl_trades['timestamp'] = pd.to_datetime(aapl_trades['timestamp'], unit='ms')

# Plotting the data or performing any analysis you need to
# Here, for example, you would calculate and plot time differences, or CPU idle times

# Assuming you logged CPU idle times in a log file
cpu_idle_times = pd.read_csv('cpu_idle_times.txt', header=None, names=['idle_time'])

# Plotting CPU idle times
plt.plot(cpu_idle_times['idle_time'])
plt.xlabel('Time (minutes)')
plt.ylabel('CPU Idle Time (%)')
plt.title('CPU Idle Time Over Execution')

# Save the plot as an image
plt.savefig('cpu_idle_time_plot.png')

# Show the plot
plt.show()
