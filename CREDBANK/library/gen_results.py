import seaborn as sb
import pandas as pd
import numpy as np
import pylab as pl
from dateutil.parser import parse
from sklearn.neighbors.kde import KernelDensity
import re
import scipy

basedir = "/home/masdarcis/Projects/dataset/CREDBANK/"
tweets_filename = "cred_event_SearchTweets_searchedtweetfile.data"
cred_filename = 'cred_event_TurkRatings.data'

def dt2mins(dtin):
    return int((dtin.toordinal()+dtin.hour/24.0+dtin.minute/(24*60.0))*10000)

def tweetlist2timestamp(tweetlist):
    tweets=re.compile("CreatedAt=(.+?)'",re.DOTALL).findall(tweetlist)
    tweetsdt=[parse(tmp) for tmp in tweets]
    tweetstamps=[dt2mins(tmp) for tmp in tweetsdt]
    min_val = np.min(tweetstamps)
    output = [x-min_val for x in tweetstamps]
    return output

def average_growth(farray):
	temp = []
	for i in range(1, len(farray)):
		value = (farray[i]-farray[i-1]) / farray[i-1]
		temp.append(value)
	return sum(temp) / len(temp)

# Loading in events' credibility scores
cred=pd.read_csv(basedir + cred_filename, sep="\t")
ratings_tmp=[eval(tmp) for tmp in cred.Cred_Ratings]
ratings=[np.mean([int(tmp) for tmp in tmp1]) for tmp1 in ratings_tmp]
cred['meanCred']=ratings
# credDict=dict(zip(cred.topic_key,cred.meanCred))

# Loading in tweets file with count, only 10 rows
# HANDLING FOR ALL TOPICS INCLUDED
tweets=pd.read_csv(basedir+tweets_filename, sep="\t", nrows=25)

# Merge dataset into 1 dataframe
cred.drop(['topic_terms','Reasons','Cred_Ratings'],axis=1, inplace=True)
dataset = pd.merge(tweets, cred, how="inner", on=['topic_key'])
dataset['kde_data'] = [np.asarray(tweetlist2timestamp(tmp)) for tmp in dataset['ListOf_tweetid_author_createdAt_tuple']]
dataset.drop(['ListOf_tweetid_author_createdAt_tuple'], axis=1, inplace=True)
dataset.sort(['meanCred'], ascending=[1], inplace=True)
dataset['b_t'] = [np.mean(x)-np.std(x) for x in dataset['kde_data']]
dataset['t_t'] = [np.mean(x)+np.std(x) for x in dataset['kde_data']]
dataset['kde_data_filtered'] = [np.asarray(x['kde_data'][(x['kde_data'] >= x['b_t']) & (x['kde_data'] <= x['t_t'])]) for index,x in dataset.iterrows()]
dataset['histogram'] = [pl.hist(x, bins=50) for x in dataset['kde_data']]
dataset['avg_growth'] = [average_growth(x[0][x[0] > 0]) for x in dataset['histogram']]

# Scatter plot for average
pl.cla()
x = np.array(dataset['meanCred'])
y = np.array(dataset['avg_growth'])
pl.scatter(x, y)
pl.show()

# # draw to analyze ROW 1 ONLY
# figure = pl.figure(figsize=(10,60))
# iterate = 1
# for index, row in dataset.iterrows():
# 	ax = figure.add_subplot(dataset.shape[0], 1, iterate)
# 	ax.annotate(str(row['meanCred']) + "  " + str(row['topic_terms']), xy=(1, 0), xytext=(-5, 5), fontsize=16, xycoords='axes fraction', textcoords='offset points', ha='right', va='bottom')

# 	# # graphical stuffs
# 	# test.append(ax.hist(row['kde_data_filtered']))
# 	# test.append(ax.hist(row['kde_data']))
# 	# temp = sb.kdeplot(np.array(row['kde_data']))
# 	# x,y = temp.get_lines()[0].get_data()
# 	# cdf = scipy.integrate.cumtrapz(y,x,initial=0)
# 	# nearest_05 = np.abs(cdf-0.5).argmin()
# 	# x_median = x[nearest_05]
# 	# y_median = y[nearest_05]
# 	# ax.vlines(x_median, 0, y_median)
	
# 	# mean = np.mean(row['kde_data'])
# 	# standev = np.std(row['kde_data'])
# 	# ax.axvline(mean, linestyle='dashed', linewidth=2, color="b")
# 	# ax.axvline(mean - standev, linestyle='dashed', linewidth=2, color="r")
# 	# ax.axvline(mean + standev, linestyle='dashed', linewidth=2, color="r")

# 	# Calculate average growth
# 	histogram = ax.hist(row['kde_data_filtered'])
# 	print histogram

# 	iterate = iterate + 1
# 	break

# # pl.show()