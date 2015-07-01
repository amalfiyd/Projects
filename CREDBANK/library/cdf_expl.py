import numpy as np
import scipy
import seaborn as sns
import matplotlib.pyplot as plt

sns.set_palette("hls", 1)
data = np.random.randn(10)
p=sns.kdeplot(data, shade=True)
c=sns.kdeplot(data, cumulative=True)

x,y = p.get_lines()[0].get_data()

cdf = scipy.integrate.cumtrapz(y, x, initial=0)
nearest_05 = np.abs(cdf-0.5).argmin()
x_median = x[nearest_05]
y_median = 1
plt.vlines(x_median, 0, y_median)
plt.show()