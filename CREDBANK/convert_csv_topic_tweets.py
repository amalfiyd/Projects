from collections import Counter
import math

base_dir = "/home/masdarcis/Projects/dataset/CREDBANK/"

fo = open(base_dir + "cred_event_SearchTweets_searchedtweetfile.data", "r")
f_tweets = open(base_dir + "topic_tweets.csv", "w")

iterate = 0
fo.readline()
for line in fo:
	str_split = line.replace("\n","").split("\t")
	topics_key = str_split[0]
	topics = str_split[1].replace(",","_")
	count = str_split[2]
	timestamp = topics_key.split("-")[1].split("_")[0]

	col3 = str_split[3].replace("[(","").replace(")]","").split("), (")
	l_ids = []
	for x in col3:
		my_id = x.split("', '")[0]
		my_id = my_id.split("=")[1]
		l_ids.append(my_id)

	temp = []
	temp.append(topics_key)
	temp.append(topics)
	temp.append(timestamp)
	temp.append(count)
	temp.append("-".join(l_ids))
	
	f_tweets.write(",".join(temp))
	f_tweets.write("\n")

	iterate = iterate + 1
	print iterate
	# if iterate == 3 :
	# 	break
print "Done!"

fo.close() 
f_tweets.close()