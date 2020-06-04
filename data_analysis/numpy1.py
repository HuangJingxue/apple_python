import pandas_datareader.data as web
import datetime
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from mpl_finance import candlestick_ohlc
from pandas.plotting import register_matplotlib_converters

register_matplotlib_converters()

today = datetime.date.today()
start = today - datetime.timedelta(days=30)
baba = web.DataReader('baba', 'yahoo', start, today)

baba_trimmed = baba.loc[:, ['Open', 'High', 'Low', 'Close']]
baba_trimmed.reset_index(inplace=True)
baba_trimmed['Date'] = baba_trimmed['Date'].map(mdates.date2num)

ax = plt.subplot()
candlestick_ohlc(ax, baba_trimmed.values, width=0.6, colorup='r', colordown='g', alpha=0.8)
ax.grid(True)
ax.set_axisbelow(True)
ax.set_title('Alibaba Share Price', color='white')
ax.figure.set_facecolor('#121212')
ax.tick_params(axis='x', colors='white')
ax.tick_params(axis='y', colors='white')
ax.xaxis_date()
plt.xticks(rotation=90)
plt.show()