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

# Loading in events' credibility scores
cred=pd.read_csv(basedir + cred_filename, sep="\t")
ratings_tmp=[eval(tmp) for tmp in cred.Cred_Ratings]
ratings=[np.mean([int(tmp) for tmp in tmp1]) for tmp1 in ratings_tmp]
cred['meanCred']=ratings
# credDict=dict(zip(cred.topic_key,cred.meanCred))

# Loading in tweets file with count, only 10 rows
tweets=pd.read_csv(basedir+tweets_filename, sep="\t", nrows=8)

# Merge dataset into 1 dataframe
cred.drop(['topic_terms','Reasons','Cred_Ratings'],axis=1, inplace=True)
dataset = pd.merge(tweets, cred, how="inner", on=['topic_key'])
dataset['kde_data'] = [tweetlist2timestamp(tmp) for tmp in dataset['ListOf_tweetid_author_createdAt_tuple']]
dataset.drop(['ListOf_tweetid_author_createdAt_tuple'], axis=1, inplace=True)
dataset.sort(['meanCred'], ascending=[1], inplace=True)

# draw to analyze ROW 1 ONLY
figure = pl.figure(figsize=(10,60))
iterate = 1
for index, row in dataset.iterrows():
	ax = figure.add_subplot(1, 1, iterate)
	ax.annotate(str(row['meanCred']) + "  " + str(row['topic_terms']), xy=(1, 0), xytext=(-5, 5), fontsize=16, xycoords='axes fraction', textcoords='offset points', 
		ha='right', va='bottom')
	temp = sb.kdeplot(np.array(row['kde_data']))
	iterate = iterate + 1
	break

x,y = temp.get_lines()[0].get_data()
cdf = scipy.integrate.cumtrapz(y,x,initial=0)

nearest_05 = np.abs(cdf-0.5).argmin()

x_median = x[nearest_05]
y_median = y[nearest_05]

pl.vlines(x_median, 0, y_median)
pl.show()