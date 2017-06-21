#encoding:utf-8
import numpy as np
from matplotlib import pyplot as plt
import math
plt.figure() # 创建图表1

x = np.linspace(-6, 6, 100)
y = [1.0 / (1+math.exp(-i)) for i in x]
plt.plot(x,y)
plt.title('sigmoid')
plt.show()
