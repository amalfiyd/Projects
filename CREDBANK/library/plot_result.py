import seaborn as sb
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from dateutil.parser import parse
from sklearn.neighbors.kde import KernelDensity
import re
import scipy

basedir = "/home/masdarcis/Projects/dataset/CREDBANK/"

# Load meanCred and avg_growth
results = pd.read_csv(basedir + "out_result.data", sep="\t")
results.sort(['meanCred'], ascending=[1], inplace=True)

# Scatter plot for average
plt.cla()
x = np.array(results['meanCred'])
y = np.array(results['avg_growth'])
plt.scatter(x, y)
plt.show()