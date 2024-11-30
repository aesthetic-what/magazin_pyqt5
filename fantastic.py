import matplotlib.pyplot as plt
import random


data_x = []
data_y = []

for x in range(100):
    data_x.append(x)

for y in range(100):
    y = y + random.randint(10, 100)
    data_y.append(y)


print(data_x, data_y)

plt.plot(data_x,data_y )
plt.show()