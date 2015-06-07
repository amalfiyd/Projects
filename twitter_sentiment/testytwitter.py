from ytwitter import Location2Country

test = ['jakarta, barat',"prague","us"]

for i in test:
	temp = Location2Country(i)
	if temp is not None and temp != "" and temp != " ":
		print temp
	else:
		print "empty"