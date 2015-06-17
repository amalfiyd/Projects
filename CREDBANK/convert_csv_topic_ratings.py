from collections import Counter
import math

base_dir = "/home/masdarcis/Projects/dataset/CREDBANK/"

fo = open(base_dir + "cred_event_TurkRatings.data", "r")
f_ratings = open(base_dir + "topic_ratings.csv", "w")

iterate = 0
fo.readline()
for line in fo:
	str_split = line.replace("\n","").split("\t")
	col0 = str_split[0]
	
	col1 = str_split[1].replace("[u'","")
	col1 = col1.replace("']", "")
	col1 = col1.split("', u'")
	col1 = "_".join(col1)

	col2 = str_split[2].replace("['", "")
	col2 = col2.replace("']", "")
	col2 = col2.split("', '")
	col2 = "_".join(col2)

	major_ratings = map(lambda x : int(x), col2.split("_"))
	average_ratings2 = sum(major_ratings) / float(len(major_ratings))
	average_ratings = math.floor(average_ratings2 * 10)/10

	c = Counter(major_ratings)
	n_2s = c.most_common()[0]
	n_2s2 = c.most_common()[len(c.most_common())-1]

	percentage = n_2s[1] / float(sum(x[1] for x in c.most_common()))
	out_val = math.floor(percentage*10)/10

	percentage2 = n_2s2[1] / float(sum(x[1] for x in c.most_common()))
	out_val2 = math.ceil(percentage2*10)/10

	timestamp = col0.split("-")[1].split("_")[0]

	temp = []
	temp.append(col0)
	temp.append(col1)
	temp.append(timestamp)
	temp.append(col2)
	temp.append(str(n_2s[0]))
	temp.append(str(out_val))
	temp.append(str(out_val2))
	temp.append(str(average_ratings))
	temp.append(str(average_ratings2))
	
	f_ratings.write(",".join(temp))
	f_ratings.write("\n")
	
	iterate = iterate + 1
	print iterate
	# if iterate == 10 :
	# 	break
print "Done!"

fo.close() 
f_ratings.close()