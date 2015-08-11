import seaborn as sb
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from dateutil.parser import parse
from sklearn.neighbors.kde import KernelDensity
import re
import scipy

basedir = "/home/masdarcis/Projects/dataset/CREDBANK/"

fileplots = ["new_out_result_1-9.data", "new_out_result_2-8.data", "new_out_result_3-7.data", "new_out_result_4-6.data"]
# fileplots = ["new_out_result_2-8.data"]
iterate = 1

for fileplot in fileplots:
	# Load meanCred and avg_growth
	results = pd.read_csv(basedir + fileplot, sep="\t")
	results.sort(['meanCred'], ascending=[1], inplace=True)

	# Scatter plot for average
	plt.subplot(4,1, iterate)
	# plt.subplot(2,1, 1)
	x = np.array(results['meanCred'])
	y = np.array(results['avg_growth'])
	# plt.scatter(x, y)
	# plt.subplot(2,1, 2)
	sb.kdeplot(x)

	iterate = iterate + 1

plt.show()