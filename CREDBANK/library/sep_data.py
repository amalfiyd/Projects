basedir = "/home/masdarcis/Projects/dataset/CREDBANK/"
tweets_filename = "cred_event_SearchTweets_searchedtweetfile.data"

f = open(basedir+tweets_filename, "r")

iterate = 0
header = f.readline().replace("\n","")
print header

result = []
for row in f:
	if iterate%50 == 0 and iterate > 0:
		print iterate 
		fo = open("out_"+str(iterate)+".data","w")
		fo.write(header + "\n")
		fo.write("\n".join(result))
		fo.close()
		result = []
		# break
	result.append(row.replace("\n",""))
	iterate = iterate + 1
	# break

f.close()