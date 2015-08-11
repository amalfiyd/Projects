import bz2
import json
import time
import os
import re
import pandas as pd

def is_topic_text(text, keywords):
	lower_text = text.lower()
	for kw in keywords:
		each_kw = kw.split(" ")
		found = True
		for word in each_kw:
			reg = '\s' + word + '\s'
			if re.search(reg, lower_text) is None:
				found = False
				break

		if found == True:
			print kw
			return kw

	return False

def read_epoch(e_time):
	return time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(e_time))

def preprocess_tweets(row,keywords):
	if row['lang'] == "en":
		output = []
		output.append(row['id'])

		temp = is_topic_text(row['text'],keywords)
		if temp:
			output.append(temp)
			output.append(row['text'])
		else:
			return None

		output.append(time.mktime(time.strptime(row['created_at'],"%a %b %d %H:%M:%S +0000 %Y")))
		output.append(row['lang'])
		output.append(row['user']['id'])

		temp = []
		if len(row['entities']['hashtags']) > 0:
			for tags in row['entities']['hashtags']:
				temp.append(tags['text'])
		if len(temp) > 0:
			output.append("#".join(temp))
		else:
			output.append(None)

		output.append(row['geo'])
		output.append(row['coordinates'])
		output.append(row['place'])
		output.append(row['user']['time_zone'])

		return output

def list_files(dir):                                                                                                  
    r = []                                                                                                            
    subdirs = [x[0] for x in os.walk(dir)]                                                                            
    for subdir in subdirs:                                                                                            
        files = os.walk(subdir).next()[2]                                                                             
        if (len(files) > 0):                                                                                          
            for file in files: 
            	if file.endswith(".bz2"):                                                                                       
                	r.append(subdir + "/" + file)                                                                         
    return sorted(r)

keywords = []
wrd_file = open("oilprice.wrd","r")
for kw in wrd_file.readlines():
	keywords.append(kw.replace("\n","").replace("\r",""))

df = pd.DataFrame(columns=('id','keywords','text','timestamp','language','user_id','hashtags','geo','coordinates','place','user_timezone'))
index = 0

basedir = "/media/masdarcis/d85e693b-e31c-4c51-8ce9-bcfaad97b9ba/"

# CHANGE THIS
currentdir = "06"
bz2files = list_files(basedir+currentdir)

for bz2file in bz2files:
	bz_file = bz2.BZ2File(bz2file)
	print bz2file
	rows = bz_file.readlines()

	for row in rows:
		temp = json.loads(row)
		
		# Check is_deleted
		if len(temp) < 24:
			continue

		tweet = preprocess_tweets(temp, keywords)
		if tweet is not None:
			# print tweet
			print str(index) + " tweets found..."
			df.loc[index] = tweet
			index = index + 1

df.to_csv("preprocessed_june14.csv", sep="\t", encoding="utf-8")
print "Done!"