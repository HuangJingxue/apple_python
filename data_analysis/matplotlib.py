import numpy as np
import matplotlib.pyplot as plt  # 导入模块

x = np.arange(0, 2 * np.pi, 0.1)
y = np.sin(x)
plt.plot(x, y)
plt.show()


# 画爱心
t = np.arange(-6, 6, 0.1)
x = 16 * np.power(np.sin(t), 3)
y = 13 * np.cos(t) - 5 * np.cos(2*t) - 2 * np.cos(3 * t) - np.cos(4)
plt.plot(x ,y, 'r')
plt.show()


#画趋势图
import matplotlib.pyplot as plt

# 时间
x = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
# 销量
y = [61, 42, 52, 72, 86, 91, 73]
# 设置字体，解决中文乱码问题
plt.rcParams['font.family'] = ['Noto Sans CJK JP']
plt.plot(x, y)
plt.show()

#编程练习
# 在下面的 收盘价.csv 中，存着百度、阿里巴巴和腾讯 2019 年每个月股票的收盘价（美元）。
# 数据共有 3 列 12 行，这三列数据分别对应的是百度、阿里巴巴和腾讯的股票收盘价，从第 1 行到第 12 行分别对应着 BAT 2019 年 1-12 月的股票收盘价。
# 请你读取 bat.csv 文件并提取出三家公司的股票收盘价，绘制出 2019 年 BAT 股票收盘价走势图。
# 拓展：BAT 是中国互联网公司三巨头的首字母缩写，这三巨头分别是百度(Baidu)、阿里巴巴(Alibaba)和腾讯(Tencent)。

import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = ['Noto Sans CJK JP']

dates = [
  '01月', '02月', '03月', '04月', '05月', '06月',
  '07月', '08月', '09月', '10月', '11月', '12月'
]

closing_bat = np.genfromtxt('收盘价.csv', delimiter=',')
closing_baidu = closing_bat[:, 0]
closing_alibaba = closing_bat[:, 1]
closing_tencent = closing_bat[:, 2]

plt.plot(dates, closing_baidu, label='百度')
plt.plot(dates, closing_alibaba, label='阿里')
plt.plot(dates, closing_tencent, label='腾讯')

plt.xlabel('时间')
plt.ylabel('收盘价(美元)')
plt.title('2019 年 BAT 股票收盘价走势')

plt.legend()
plt.show()

# 收盘价.csv
'''
172.63,168.49,44.36
162.54,183.03,43.05
164.85,182.45,46.28
166.23,185.57,49.74
110.00,149.26,41.79
117.36,169.45,45.21
111.70,173.11,47.21
104.47,175.03,41.64
102.76,167.23,42.33
101.85,176.67,41.13
118.53,200.00,42.54
126.40,212.10,48.15
'''

#降水量和蒸发量对比
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = ['Noto Sans CJK JP']

times = ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月']
# 蒸发量
data1 = [2.0, 4.9, 7.0, 23.2, 25.6, 76.7, 135.6, 162.2, 32.6, 20.0, 6.4, 3.3]
# 降水量
data2 = [2.6, 5.9, 9.0, 26.4, 28.7, 70.7, 175.6, 182.2, 48.7, 18.8, 6.0, 2.3]
# 折线图
plt.title('2019 年一年中蒸发量和降水量对比')
plt.plot(times,data1,label='蒸发量')
plt.plot(times,data2,label='降水量')
plt.xlabel('时间')
plt.ylabel('水量')
plt.legend()
plt.show()


import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = ['Noto Sans CJK JP']

times = ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月']
# 蒸发量
data1 = [2.0, 4.9, 7.0, 23.2, 25.6, 76.7, 135.6, 162.2, 32.6, 20.0, 6.4, 3.3]
# 降水量
data2 = [2.6, 5.9, 9.0, 26.4, 28.7, 70.7, 175.6, 182.2, 48.7, 18.8, 6.0, 2.3]
# 分组柱图
x = np.arange(12)
width = 0.3
plt.bar(x - width / 2,data1,width=width,label='蒸发量')
plt.bar(x + width / 2,data2,width=width,label='降水量')
plt.xticks(x, times)
plt.title('2019 年蒸发量和降水量对比图')
plt.xlabel('时间')
plt.ylabel('水量(毫米)')
plt.legend()
plt.show()

# 饼图
#人口普查显示
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = ['Noto Sans CJK JP']

data = [59428036, 263535521, 484750032, 185402141, 68608795, 45625173, 4138550]
labels = ['没上过学', '小学', '初中', '高中', '大学专科', '大学本科', '研究生']
explode = (0, 0, 0.1, 0, 0, 0, 0)

plt.pie(data, explode=explode, labels=labels, autopct='%0.1f%%')
plt.show()

# 子图
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = ['Noto Sans CJK JP']

x = np.arange(0, 2 * np.pi, 0.1)

plt.suptitle('三角函数可视化')

ax1 = plt.subplot(2, 2, 1)
y1 = np.sin(x)
ax1.plot(x, y1)
ax1.set_title('sin 函数')




ax2 = plt.subplot(2, 2, 2)
y2 = np.cos(x)
ax2.plot(x, y2, 'r')
ax2.set_title('cos 函数')

ax3 = plt.subplot(2, 1, 2)
y3 = np.tan(x)
ax3.plot(x, y3, 'r')
ax3.set_title('tan 函数')


ax4 = plt.subplot(3, 1, 2)
data = [59428036, 263535521, 484750032, 185402141, 68608795, 45625173, 4138550]
labels = ['没上过学', '小学', '初中', '高中', '大学专科', '大学本科', '研究生']
explode = (0, 0, 0.1, 0, 0, 0, 0)

ax4.plt.pie(data, explode=explode, labels=labels, autopct='%0.1f%%')

plt.show()

# 升级练习
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = ['Noto Sans CJK JP']

x = np.arange(0, 2 * np.pi, 0.1)

plt.suptitle('三角函数可视化')

ax1 = plt.subplot(3, 2, 1)
y1 = np.sin(x)
ax1.plot(x, y1)
ax1.set_title('sin 函数')

ax2 = plt.subplot(3, 2, 2)
y2 = np.cos(x)
ax2.plot(x, y2, 'r')
ax2.set_title('cos 函数')

ax3 = plt.subplot(3, 1, 2)
y3 = np.tan(x)
ax3.plot(x, y3, 'r')
ax3.set_title('tan 函数')

ax4 = plt.subplot(3, 1, 3)
data = [59428036, 263535521, 484750032, 185402141, 68608795, 45625173, 4138550]
labels = ['没上过学', '小学', '初中', '高中', '大学专科', '大学本科', '研究生']
explode = (0, 0, 0.1, 0, 0, 0, 0)

ax4.pie(data, explode=explode, labels=labels, autopct='%0.1f%%')

plt.show()

# 高级练习
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = ['Noto Sans CJK JP']

closing_bat = np.genfromtxt('收盘价.csv', delimiter=',')
vol_bat = np.genfromtxt('成交量.csv', delimiter=',')

labels = ['百度', '阿里巴巴', '腾讯']
dates = [
  '01月', '02月', '03月', '04月', '05月', '06月',
  '07月', '08月', '09月', '10月', '11月', '12月'
]


closing_baidu = closing_bat[:, 0]
closing_alibaba = closing_bat[:, 1]
closing_tencent = closing_bat[:, 2]


vol_baidu = vol_bat[:, 0]
vol_alibaba = vol_bat[:, 1]
vol_tencent = vol_bat[:, 2]

plt.suptitle('2019 BAT股票分析')


closing_data = [np.sum(closing_baidu),np.sum(closing_alibaba),np.sum(closing_tencent)]
vol_data = [np.sum(vol_baidu),np.sum(vol_alibaba),np.sum(vol_tencent)]


ax1 = plt.subplot(2, 2, 1)
ax1.bar(labels,closing_data)
ax1.set_title('平均收盘价对比')


ax2 = plt.subplot(2, 2, 2)
ax2.pie(vol_data,  labels=labels, autopct='%0.1f%%')
ax2.set_title('日平均成交量')

ax3 = plt.subplot(2,1,2)
ax3.plot(dates, closing_baidu, 'ro-')
ax3.plot(dates, closing_alibaba,'bo-')
ax3.plot(dates, closing_tencent, 'yo-')
ax3.set_title('股价趋势')

plt.show()

#收盘价
"""
172.63,168.49,44.36
162.54,183.03,43.05
164.85,182.45,46.28
166.23,185.57,49.74
110.00,149.26,41.79
117.36,169.45,45.21
111.70,173.11,47.21
104.47,175.03,41.64
102.76,167.23,42.33
101.85,176.67,41.13
118.53,200.00,42.54
126.40,212.10,48.15
"""
#成交量
"""
64.38,361.43,441.16
62.13,223.66,257.31
56.20,233.50,407.13
67.23,260.69,295.36
134.02,511.79,455.34
75.05,431.89,306.73
60.92,356.34,238.08
112.16,405.88,418.39
73.69,247.36,288.42
63.37,261.61,332.55
95.12,409.33,357.50
60.23,301.21,346.82
"""
