import numpy as np
# 单层嵌套列表
nested_list = [[1, 2], [3, 4]]
# print(nested_list)
# 输出：[[1, 2], [3, 4]]

# 二维数组
data = np.array(nested_list)
# print(data)
# 输出：
# [[1 2]
#  [3 4]]

ones = np.ones((2, 2))
# print(ones)
# 输出：
# [[1. 1.]
#  [1. 1.]
#  [1. 1.]]

zeros = np.zeros((3, 2))
# print(zeros)
# 输出：
# [[0. 0.]
#  [0. 0.]
#  [0. 0.]]

# 认识几个描述多维数组的属性：
data = np.array([[1, 2, 3], [4, 5, 6]])
# print('ndim:', data.ndim)
# print('shape:', data.shape)
# print('size:', data.size
# print('dtype:', data.dtype)
# 输出：
# ndim: 2
# shape: (2, 3)
# size: 6
# dtype: int64

#较为复杂的二维数组并存到了变量 data 中
import numpy as np

data = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9], [1, 2, 3], [4, 5, 6],
                 [7, 8, 9], [1, 2, 3], [4, 5, 6], [7, 8, 9], [1, 2, 3],
                 [4, 5, 6], [7, 8, 9], [1, 2, 3], [4, 5, 6], [7, 8, 9]])

# print('data 的行数为：', data.ndim)
# print('data 的元素个数为：', data.size)

# 数组形状不同
data = np.array([[1, 2], [3, 4], [5, 6]])
ones = np.ones(2)
# print(data.shape)
# print(ones.shape)
# 输出：
# (3, 2)
# (2,)


# 测试数据形状不同何时无法进行广播，进行修正
import numpy as np

data = np.array([[1, 2, 3], [4, 5, 6]])
ones = np.ones(2)
# print(data.shape)
# print(ones.shape)
# print(data + ones)

# 了解axis
# data = np.array([[1, 2], [5, 3], [4, 6]])
# print(data)

# 不指定 axis
# print(data.max())
# 输出：6

# axis=0
# print(data.max(axis=0))
# 输出：[5 6]

# axis=1
# print(data.max(axis=1))
# 输出：[2 5 6]

# 计算二维数组在行轴方向上的和
import numpy as np
data = np.array([[1, 2, 3], [4, 5, 6]])
# print(data.sum(axis=0))

# 二维数组的索引和分片
data = np.array([[1, 2], [3, 4], [5, 6]])

# print(data[0, 1])
# 输出：2

# print(data[:, 0])
# 输出：[1 3 5]

# print(data[1:3])
# 输出：
# [[3 4]
#  [5 6]]

# 布尔索引
data = np.array([[1, 2], [3, 4], [5, 6]])
print(data[data > 3])
# 输出：[4 5 6]

data = np.array([[1, 2], [3, 4], [5, 6]])
# 大于 3 或者小于 2
print(data[(data > 3) | (data < 2)])
# 输出：[1 4 5 6]

# 大于 3 或者不小于 2（即大于等于 2）
print(data[(data > 3) | ~(data < 2)])
# 输出：[2 3 4 5 6]


# 二维数组中所有大于平均数的元素并将其打印出来。
import numpy as np

data = np.array([[23, 12, 55], [7, 34, 66], [8, 16, 27]])
dmean = np.mean(data)
print(data[data > np.mean(data)])

# 实用方法
# 生产随机数组
# 生成 1-9 的数组
print(np.arange(1, 10))
# 输出：[1 2 3 4 5 6 7 8 9]

# 生成 0-9 的数组
print(np.arange(10))
# 输出：[0 1 2 3 4 5 6 7 8 9]

# 生成 1-9 的数组，步长为 2
print(np.arange(1, 10, 2))
# 输出：[1 3 5 7 9]

# 不传入形状时
print(np.random.randint(0, 5))
# 输出：3

# 形状为一维数组时
print(np.random.randint(0, 5, 3))
# 输出：[4 0 1]

# 形状为二维数组时
print(np.random.randint(0, 5, (2, 3)))
# 输出：
# [[0 2 1]
#  [4 2 0]]

# 均方误差公式
"""
labels.csv 
46,13,23,81,51,66,80,52,67,62
26,35,97,11,98,40,77,96,26,24
56,40,15,71,59,52,40,53,48,30
28,73,45,67,99,11,32,36,31,40
30,31,20,29,23,70,83,90,34,62
39,57,13,94,13,30,27,52,46,58
63,55,22,30,41,86,32,74,83,40
19,39,53,25,24,93,87,78,28,43
67,75,52,92,41,42,38,45,35,63
74,58,67,59,18,16,85,90,43,65

predictions.csv
43,11,20,79,49,66,77,50,67,60
26,35,96,17,96,39,74,94,23,22
55,40,12,71,57,49,38,51,45,30
27,71,43,63,95,11,31,32,30,36
29,31,19,25,23,69,83,89,32,61
37,54,13,94,11,26,23,48,43,56
59,52,19,28,38,86,30,72,80,39
15,37,49,21,22,89,86,76,24,40
67,73,52,91,41,38,37,45,35,63
71,55,65,56,18,13,83,86,39,65
"""


import numpy as np

labels = np.genfromtxt('labels.csv',delimiter=',')
# print(labels)
predictions = np.genfromtxt('predictions.csv',delimiter=',')
errors = (1 / labels.size) * np.sum(np.square(predictions - labels))
print(errors)