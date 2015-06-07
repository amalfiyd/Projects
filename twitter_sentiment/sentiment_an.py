import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import re
import os
from textblob import TextBlob

# get polarity for each text
def sentiment_an(df):
	result = []
	newdf = df
	for text in df[2]:
		temp = re.sub(r'[^\x00-\x7f]',r' ',text.replace("\n",""))
		blob = TextBlob(temp)
		result.append(blob.sentiment.polarity)
	e = pd.Series(result)
	newdf[newdf.shape[1]] = e
	return newdf

# file iterator
def list_files(dir):                                                                                                  
    r = []                                                                                                            
    subdirs = [x[0] for x in os.walk(dir)]                                                                            
    for subdir in subdirs:                                                                                            
        files = os.walk(subdir).next()[2]                                                                             
        if (len(files) > 0):                                                                                          
            for file in files: 
            	if file.endswith(".csv"):                                                                                       
                	r.append(subdir + "/" + file)                                                                         
    return r   

rootdirs = []
# February
rootdir = "/home/aydarusman/Documents/Conference Stuff/data_processing/0214"
rootdirs.append(rootdir)
# March
rootdir = "/home/aydarusman/Documents/Conference Stuff/data_processing/0314"
rootdirs.append(rootdir)
# April
rootdir = "/home/aydarusman/Documents/Conference Stuff/data_processing/0414"
rootdirs.append(rootdir)
# May
rootdir = "/home/aydarusman/Documents/Conference Stuff/data_processing/0514"
rootdirs.append(rootdir)

outputfile = open("res_sentiment.txt", "w")
filenames = list_files(rootdir)

plotposcount = []
plotnegcount = []
plotnetcount = []
sentimentscore = []
feb = ["1-7 Feb","8-14 Feb","15-21 Feb","22-28 Feb"]
mar = ["1-7 Mar","8-14 Mar","15-21 Mar","22-28 Mar"]
apr = ["29-4 Apr","5-11 Apr","12-18 Apr","19-25 Apr"]
may = ["26-2 May","3-9 May","10-16 May","17-23 May", "24-30 May"]

axis = feb + mar + apr + may
# axis = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17]

for dir in rootdirs:
	outputfile.write("Month : " + dir.split("/")[6])
	outputfile.write(os.linesep)
	filenames = list_files(dir)
	for file in sorted(filenames):
		weekname = file.split("/")[7].split(".")[0]

		df = pd.read_csv(file, header=None)
		weekname = file.split("/")[7].split(".")[0]
		outputfile.write(weekname)
		outputfile.write(os.linesep)

		newdf = sentiment_an(df)
		scorepos = 0
		scoreneg = 0
		countnet = 0
		countpos = 0
		countneg = 0
		sentimenttemp = []

		for sentiment in newdf[15]:
			if sentiment > 0:
				scorepos += sentiment
				countpos += 1
			elif sentiment < 0:
				scoreneg += sentiment
				countneg += 1
			else:
				countnet += 1

			sentimenttemp.append(sentiment)

		sentimentscore.append(np.mean(sentimenttemp))

		# outputfile.write("poscount : " + str(countpos))
		# outputfile.write(os.linesep)
		# plotposcount.append(countpos)
		# # outputfile.write("posavg : " + str(scorepos/countpos))
		# # outputfile.write(os.linesep)
		# outputfile.write("negcount : " + str(countneg))
		# outputfile.write(os.linesep)
		# plotnegcount.append(countneg)
		# # outputfile.write("negavg : " + str(scoreneg/countneg))
		# # outputfile.write(os.linesep)
		# outputfile.write("neutcount : " + str(countnet))
		# outputfile.write(os.linesep)
		# plotnetcount.append(countnet)

	outputfile.write(os.linesep)

outputfile.close()

x = np.arange(17)
fig, ax = plt.subplots()
fig.canvas.draw()
ax.set_xticks(x)
ax.set_xticklabels(axis, rotation=45)
plt.plot(sentimentscore, color='b')

plt.show()