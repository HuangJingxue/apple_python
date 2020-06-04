import numpy as np

data = np.array([1, 2, 3,5])
print(data)
# 输出：[1 2 3]
print(type(data))
# 输出：<class 'numpy.ndarray'>

ones = np.ones(3)
print(ones)
# 输出：[1. 1. 1.]

zeros = np.zeros(3)
print(zeros)
# 输出：[0. 0. 0.]
print(ones+zeros)
# 输出：[1. 1. 1.]


ones = np.ones(3, dtype='int')
print(ones)
# 输出：[1 1 1]
zeros = np.zeros(3, dtype='int')
print(zeros)
# 输出：[0 0 0]

data = np.array([1,2,3,np.ones(3)])
print(data)
# 输出：[1 2 3 array([1., 1., 1.])]

# 多维数组的加减乘除
data = np.array([1, 2])
ones = np.ones(2)
print(data + ones)
# 输出：[2. 3.]

#多维数组直接和数字进行计算
data = np.array([1, 2])
print(data + 1)
# 输出：[2 3]

#下面的数组 [1 2 3] 经过运算得到数组 [2. 2. 2.]
import numpy as np

data = np.array([1, 2, 3])
print(data * 2 / data)

#了解索引和分片
data = np.array([1, 2, 3])
print(data[0:2])  # 获取索引为 0 和 1 的元素
# 输出：[1 2]

# 列表
lst_data = [1, 2, 3]
lst_data2 = lst_data[:]
lst_data2[0] = 6
print(lst_data)
# 输出：[1, 2, 3]

# 多维数组
arr_data = np.array([1, 2, 3])
arr_data2 = arr_data[:]
arr_data2[0] = 6
print(arr_data)
# 输出：[6 2 3]

data = np.array([1, 2, 3, 4, 5, 6])
print(data[::2])  # 省略前两个参数
# 输出：[1 3 5]

#练习1
import numpy as np
data = np.array([1, 2, 3, 4, 5, 6])
# 打印前 3 个元素
print(data[:3])
# 打印后 2 个元素
print(data[-2:])
# 打印反转后的元素
print(data[::-1])

#推荐首发球员
import numpy as np

player1 = np.array([7, 9, 10, 9, 11, 13, 10, 10, 11, 10])
player2 = np.array([7, 9, 8, 9, 11, 10, 11, 12, 10, 13])
player3 = np.array([3, 7, 10, 3, 6, 30, 10, 7, 11, 13])

print('球员1得分的平均数为', np.mean(player1))
print('球员2得分的平均数为', np.mean(player2))
print('球员3得分的平均数为', np.mean(player3))
print('====================')
print('球员1得分的中位数为', np.median(player1))
print('球员2得分的中位数为', np.median(player2))
print('球员3得分的中位数为', np.median(player3))
print('====================')
print('球员1得分的标准差为', np.std(player1))
print('球员2得分的标准差为', np.std(player2))
print('球员3得分的标准差为', np.std(player3))
'''
球员1得分的平均数为 10.0
球员2得分的平均数为 10.0
球员3得分的平均数为 10.0
====================
球员1得分的中位数为 10.0
球员2得分的中位数为 10.0
球员3得分的中位数为 8.5
====================
球员1得分的标准差为 1.4832396974191326
球员2得分的标准差为 1.7320508075688772
球员3得分的标准差为 7.362064927722384
'''
