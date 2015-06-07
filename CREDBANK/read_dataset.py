# fo = open("../stream_tweets_byTimestamp.data", "r")
fo = open("../cred_event_SearchTweets.data", "r")
# fo = open("../cred_event_TurkRatings.data", "r")
# fo = open("../eventNonEvent_annotations.data", "r")
# fo = open("../topic_tweets.csv", "r")
# f1 = open("../f_1.data", "w")
# f2 = open("../f_2.data", "w")
f3 = open("../f_3.data", "w")
# f_events = open("../events_list.data", "w")

counter = 0
iterate = 0
fo.readline()
for line in fo:
	temp = line.split("\t")
	f3.write(temp[1] + "\n")
	iterate = iterate + 1
	print iterate
	if iterate == 100:
		break
# print "Total : ", iter

# f_r1 = fo.readline()
# f_r2 = fo.readline()

# f1.write(f_r1)
# f2.write(f_r2)

fo.close()
f3.close() 
# f1.close()
# f2.close()