base_dir = "/home/masdarcis/Projects/dataset/CREDBANK/"

fo = open(base_dir + "cred_event_TurkRatings.data", "r")
f_ratings = open(base_dir + "topic_ratings.csv", "w")

iterate = 0
fo.readline()
for line in fo:
	str_split = line.split("\t")
	col0 = str_split[0]
	col1 = int(str_split[1])
	col2 = str_split[2].replace("[u'","")
	print col2
	


	iterate = iterate + 1
	# print iterate
	break
print "Done!"

fo.close() 
f_totweets.close()