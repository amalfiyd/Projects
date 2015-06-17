from collections import Counter
import math

base_dir = "/home/masdarcis/Projects/dataset/CREDBANK/"

fo = open(base_dir + "eventNonEvent_annotations.data", "r")
f_isevent = open(base_dir + "topic_isevent.csv", "w")

iterate = 0
fo.readline()
for line in fo:
	str_split = line.replace("\n","").split("\t")
	col0 = str_split[0]
	col1 = str_split[1]
	col2 = str_split[2]
	timestamp = col0.split("-")[0].split("_")[0]
	topics = col1.replace(",","_")
	
	temp = []
	temp.append(topics)
	temp.append(timestamp)
	temp.append(col2)
	
	f_isevent.write(",".join(temp))
	f_isevent.write("\n")

	iterate = iterate + 1
	print iterate
	# if iterate == 10 :
	# 	break
print "Done!"

fo.close() 
f_isevent.close()