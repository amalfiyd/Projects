f = open("/home/masdarcis/Projects/dataset/CREDBANK/separated_searchtweets/out_50.data","r")

for row in f:
	test = row.split("\t")
	print test[0]
	break