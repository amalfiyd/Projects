base_dir = "/home/masdarcis/Projects/dataset/CREDBANK/"

fo = open(base_dir + "stream_tweets_byTimestamp.data", "r")
# fo = open("../cred_event_SearchTweets.data", "r")
# fo = open("../cred_event_TurkRatings.data", "r")
# fo = open("../eventNonEvent_annotations.data", "r")
# f_events = open("../topic_isevent.csv", "w")
# f_ratings = open("../topic_ratings.csv", "w")
f_totweets = open("tweets_timestamp.csv", "w")

iterate = 0
fo.readline()
for line in fo:
	str_split = line.split("\t")
	col0 = str_split[0]
	col1 = int(str_split[1])
	col2 = str_split[2].replace("[(","")
	col2 = col2.replace(")]","")
	processing = col2.split("), (")
	for pl in processing:
		# HERE HERE HERE

	# processing = str_split[3].replace("[(","").replace(")]\n","").split("), (")
	# allids = []
	# for pl in processing:
	# 	test = pl.replace("\n","").replace("'ID=","").split("', '")
	# 	allids.append(test[0].replace("\n",""))
	# # col3 = str_split[3].replace("['","").replace("']","").replace("', '","-")
	# temp = col0 + "," + col1 + "," + col2 + "," + "-".join(allids)
	# f_totweets.write(temp.replace("\n","") + "\n")
	
	iterate = iterate + 1
	print iterate
	# break
print "Done!"

fo.close() 
f_totweets.close()