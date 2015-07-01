import seaborn as sb
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from dateutil.parser import parse
from sklearn.neighbors.kde import KernelDensity
import re
import scipy

basedir = "/home/masdarcis/Projects/dataset/CREDBANK/"
searchdir = basedir + "separated_searchtweets/"
tweets_filenames = []
cred_filename = 'cred_event_TurkRatings.data'

# WARNING OUT DATA
out_file = open(basedir + "out_result.data","w")
out_file.write("meanCred\tavg_growth\n")

# Functions
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
    if len(temp) == 0:
        return 0
    else:
        return sum(temp) / len(temp)

# Prepare the tweet_filenames
x = 50
while x <= 1350:
    tweets_filenames.append(searchdir + "out_" + str(x) + ".data")
    x = x + 50

# TEMP
# tweets_filenames.append(searchdir + "out_600.data")

# Loading in events' credibility scores
cred=pd.read_csv(basedir + cred_filename, sep="\t")
ratings_tmp=[eval(tmp) for tmp in cred.Cred_Ratings]
ratings=[np.mean([int(tmp) for tmp in tmp1]) for tmp1 in ratings_tmp]
cred['meanCred']=ratings
cred.drop(['topic_terms','Reasons','Cred_Ratings'],axis=1, inplace=True)
    
# Load and Write meanCred and avg_growth
for tweet_file in tweets_filenames:
    print tweet_file

    # Loading in tweets file with count
    tweets=pd.read_csv(tweet_file, sep="\t")

    # Merge dataset into 1 dataframe
    dataset = pd.merge(tweets, cred, how="inner", on=['topic_key'])
    dataset['kde_data'] = [np.asarray(tweetlist2timestamp(tmp)) for tmp in dataset['ListOf_tweetid_author_createdAt_tuple']]
    dataset.drop(['ListOf_tweetid_author_createdAt_tuple'], axis=1, inplace=True)
    dataset.sort(['meanCred'], ascending=[1], inplace=True)

    b_t = []
    t_t = []
    for iterate in dataset.kde_data.iteritems():
        print iterate
        kdetemp = sb.kdeplot(iterate[1], cumulative=True)
        xc,yc = kdetemp.get_lines()[0].get_data()
        s1 = pd.Series(xc, name="x")
        s2 = pd.Series(yc, name="y")
        pddf = pd.concat([s1,s2], axis=1)
        df_process = pddf[(pddf.y >= 0.1) & (pddf.y <= 0.9)]
        if len(df_process > 0):
            b_t.append(df_process.head(1).x.item())
            t_t.append(df_process.tail(1).x.item())
        else:
            b_t.append(1)
            t_t.append(-1)
        plt.clf()
    
    dataset['b_t'] = b_t
    dataset['t_t'] = t_t
    dataset['kde_data_filtered'] = [np.asarray(x['kde_data'][(x['kde_data'] >= x['b_t']) & (x['kde_data'] <= x['t_t'])]) for index,x in dataset.iterrows()]
    dataset['histogram'] = [plt.hist(x, bins=50) if (len(x) > 0) else 0 for x in dataset['kde_data_filtered']]
    dataset['avg_growth'] = [average_growth(x[0][x[0] > 0]) if (x != 0) else 0 for x in dataset['histogram']]

    plt.clf()

    for i in dataset[['meanCred', 'avg_growth']].iterrows():
        out_string = str(i[1][0]) + "\t" + str(i[1][1]) + "\n"
        out_file.write(out_string)

    # break

out_file.close()

# # Load meanCred and avg_growth
# results = pd.read_csv(basedir + "out_result.data", sep="\t")
# results.sort(['meanCred'], ascending=[1], inplace=True)

# # Scatter plot for average
# pl.cla()
# x = np.array(results['meanCred'])
# y = np.array(results['avg_growth'])
# pl.scatter(x, y)
# pl.show()

# ------------------------------

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