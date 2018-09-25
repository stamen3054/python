import numpy as np
from matplotlib import pyplot as plt

# 柱状图
num_list = [3600, 5500, 4500]
plt.bar(range(len(num_list)), num_list, tick_label=['Male', 'Female', 'Unknown'])
plt.show()

# 堆叠柱状图
dob_list = ['1989', '1990', '1991', '1992']
num_list_male = [2000, 3000, 1500, 1300]
num_list_female = [1500, 4000, 2700, 1500]
num_list_unknown = [100, 500, 1000, 3000]
num_list_unknown_bottom = [3500, 7000, 4200, 2800]
plt.bar(range(len(num_list_male)), num_list_male, label='male', fc='y')
plt.bar(range(len(num_list_female)), num_list_female, label='female', bottom=num_list_male, fc='r')
plt.bar(range(len(num_list_unknown)), num_list_unknown, label='unknown', bottom=num_list_unknown_bottom,
        tick_label=dob_list,
        fc='g')
plt.legend()
plt.show()

# 平行柱状图
x = list(range(len(num_list_male)))
total_width, n = 0.8, 2
width = total_width / 3

plt.bar(x, num_list_male, width=width, label='male', fc='y')
for i in range(len(x)):
    x[i] = x[i] + width
plt.bar(x, num_list_female, width=width, label='female', fc='r')
for i in range(len(x)):
    x[i] = x[i] + width
plt.bar(x, num_list_unknown, width=width, label='unknown', fc='g')
plt.legend()
plt.show()

# 线型图
x = np.linspace(-30, 50)
y = np.linspace(-30, 47)
plt.plot(x, y)
plt.show()
