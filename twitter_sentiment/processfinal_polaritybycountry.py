import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from textblob import TextBlob

def sentimen(string):
	return TextBlob(string).sentiment.polarity

files = ["preprocessed/feb_set2.csv", "preprocessed/mar_set2.csv", "preprocessed/apr_set2.csv", "preprocessed/may_set2.csv"]
feb = ["1-7 Feb","8-14 Feb","15-21 Feb","22-28 Feb"]
mar = ["1-7 Mar","8-14 Mar","15-21 Mar","22-28 Mar"]
apr = ["29-4 Apr","5-11 Apr","12-18 Apr","19-25 Apr"]
may = ["26-2 May","3-9 May","10-16 May","17-23 May", "24-30 May"]

timeseries = feb + mar + apr + may

df1 = pd.read_csv(files[0], header=None)
df2 = pd.read_csv(files[1], header=None)
df3 = pd.read_csv(files[2], header=None)
df4 = pd.read_csv(files[3], header=None)
dffinal = pd.concat([df1, df2, df3, df4])

dffinal['polarity'] = dffinal[2].apply(lambda x: sentimen(x))
cp = dffinal.groupby(dffinal[3])

# # Plotting 
# x = np.arange(17)
# fig, ax = plt.subplots()
# fig.canvas.draw()
# ax.set_xticks(x)
# ax.set_xticklabels(timeseries, rotation=45)
# plt.plot(polarcountry, color='b')
# plt.show()