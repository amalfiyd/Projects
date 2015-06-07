from collections import Counter

base_url = "/home/masdarcis/Projects/dataset/CREDBANK/"
fo = open(base_url + "stream_tweets_byTimestamp.data", "r")
# fo = open("..cred_event_SearchTweets.data", "r")
# fo = open(base_url+"cred_event_TurkRatings.data", "r")
# fo = open("eventNonEvent_annotations.data", "r")
# fo = open("topic_tweets.csv", "r")
# f1 = open("f_1.data", "w")
# f2 = open("f_2.data", "w")
# f3 = open("f_3.data", "w")
# f_events = open("events_list.data", "w")

counter = 0
iterate = 0
fo.readline()
for line in fo:
	temp = line.split("\t")
	values = temp[2]
	values = values.replace("['","")
	values = values.replace("']","")
	my_list = values.split("', '")
	my_list = map(lambda x : int(x), my_list)
	c = Counter(my_list)
	major_rating, count = c.most_common()[0]

	if major_rating < 2:
		counter = counter + 1

	# f3.write(temp[1] + "\n")
	iterate = iterate + 1
	print iterate

	if iterate == 1:
		break

print "Total : ", counter

# f_r1 = fo.readline()
# f_r2 = fo.readline()

# f1.write(f_r1)
# f2.write(f_r2)

fo.close()
# f3.close() 
# f1.close()
# f2.close()