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
weeklypol = []

for filename in files:
	df = pd.read_csv(filename, header=None)

	# Weekly Polarity
	df['polarity'] = df[2].apply(lambda x: sentimen(x))
	wp = df['polarity'].groupby(df[6])

	temp = wp.mean()
	for i in temp:
		weeklypol.append(i)

# Plotting 
x = np.arange(17)
fig, ax = plt.subplots()
fig.canvas.draw()
ax.set_xticks(x)
ax.set_xticklabels(timeseries, rotation=45)
plt.plot(weeklypol, color='b')
plt.show()