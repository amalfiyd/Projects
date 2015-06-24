import pickle,time,re, jsonpickle

tweets = pickle.load(open("twitterstream_Sat_Jun_20_14:13:55_2015.pkl","rb"))
# f = open('seewhathappens.result',"w+")
temp = []
for i in range(0,1000000):
	print i
	temp.append(tweets[0])

# f.write("\n".join(temp))
# f.close()

print "Finish!!!"