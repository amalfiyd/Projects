import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import re
import os
from textblob import TextBlob

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

# Count tweet weekly
def count_tweet(df):
	return df.shape[0]

rootdirs = []
rootdir = "/home/aydarusman/Documents/Conference Stuff/data_processing/0214"
rootdirs.append(rootdir)
rootdir = "/home/aydarusman/Documents/Conference Stuff/data_processing/0314"
rootdirs.append(rootdir)
rootdir = "/home/aydarusman/Documents/Conference Stuff/data_processing/0414"
rootdirs.append(rootdir)
rootdir = "/home/aydarusman/Documents/Conference Stuff/data_processing/0514"
rootdirs.append(rootdir)

outfile = open("res_tweetcount.txt","w")

plottweetcount = []
feb = ["1-7 Feb","8-14 Feb","15-21 Feb","22-28 Feb"]
mar = ["1-7 Mar","8-14 Mar","15-21 Mar","22-28 Mar"]
apr = ["29-4 Apr","5-11 Apr","12-18 Apr","19-25 Apr"]
may = ["26-2 May","3-9 May","10-16 May","17-23 May", "24-30 May"]
axis = feb + mar + apr + may

for dir in rootdirs:
	outfile.write("Month : " + dir.split("/")[6])
	outfile.write(os.linesep)
	filenames = list_files(dir)

	for file in sorted(filenames):
		df = pd.read_csv(file, header=None)
		weekname = file.split("/")[7].split(".")[0]

		# outfile.write(os.linesep)
		outfile.write(weekname)
		temp = count_tweet(df)
		plottweetcount.append(temp)
		# outfile.write(os.linesep)
		outfile.write(" : " + str(temp) + os.linesep)
		# outfile.write(os.linesep)c
	outfile.write(os.linesep)

outfile.close()

x = np.arange(17)
fig, ax = plt.subplots()
fig.canvas.draw()
ax.set_xticks(x)
ax.set_xticklabels(axis, rotation=70)
plt.plot(plottweetcount, color='b')

plt.show()