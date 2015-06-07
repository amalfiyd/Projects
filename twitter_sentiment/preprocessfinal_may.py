import bz2, os, math, json, subprocess, sys
# from ytwitter import Location2Country

def untarbz2(basefile, outfile):
	tar = bz2.BZ2File(basefile)
	data = tar.read()
	filez = open(outfile, 'wb')
	filez.write(data)
	filez.close()

def list_files(dir):                                                                                                  
    r = []                                                                                                            
    subdirs = [x[0] for x in os.walk(dir)]                                                                            
    for subdir in subdirs:                                                                                            
        files = os.walk(subdir).next()[2]                                                                             
        if (len(files) > 0):                                                                                          
            for file in files: 
            	if file.endswith(".bz2"):                                                                                       
                	r.append(subdir + "/" + file)                                                                         
    return r  

def _jsontocsv(jsoninput, allowedhash, notallowedhash):

	# The conversion algorithm
	obj = json.loads(jsoninput)
	outvalue = None

	t_id = None
	t_createdate = None
	t_text = None
	# t_coordinates = None
	t_place = None
	# t_favoritecount = None
	# t_retweetcount = None
	# t_lang = None
	# u_id = None
	# u_name = None
	u_location = None
	# u_followerscount = None
	# u_friendscount = None
	# u_createdate = None
	e_count = None
	e_text = None

	for ka, va in obj.iteritems():
		if ka == "delete":
			return -1
		if ka == "id":
			t_id = va
		elif ka == "created_at":
			t_createdate = va
		elif ka == "text":
			# CLEAN FROM NOT ALLOWED HASH
			for notokay in notallowedhash:
				if notokay in va.lower():
					return -1 
			# CONTEXT RELATION ON TEXT
			# brocounter = 0
			# for okay in allowedhash:
			# 	temp = okay.replace("\n", "").lower()
			# 	if temp in va.lower():
			# 		brocounter = brocounter + 1
			# if brocounter <= 1:
			# 	return -1
			t_text = va
		# elif ka == "coordinates":
		# 	if va is not None:
		# 		for kb, vb in va.iteritems():
		# 			if kb == "coordinates":
		# 				t_coordinates = vb
		# 				break
		# 	else:
		# 		t_coordinates = "null"
		elif ka == "place":
			if va is not None:
				for kb, vb in va.iteritems():
					if kb == "country_code":
						if vb is not None or vb != "":
							t_place = vb
						else:
							t_place = "null"
						break
			else:
				t_place = "null"
		# elif ka == "favorite_count":
		# 	t_favoritecount = va
		# elif ka == "retweet_count":
		# 	t_retweetcount = va
		elif ka == "lang":
			if va != "en":
				return -1
			# else:
			# 	t_lang = va
		elif ka == "user":
			if va is not None:
				for kb, vb in va.iteritems():
					# if kb == "id":
					# 	u_id = vb
					# elif kb == "name":
					# 	u_name = vb
					if kb == "location":
						if vb != "" or vb is not None:
							u_location = vb
						else:
							u_location = "null"
						break
					# elif kb == "followers_count":
					# 	u_followerscount = vb
					# elif kb == "friends_count":
					# 	u_friendscount = vb
					# elif kb == "created_at":
					# 	u_createdate = vb
			else:
				# u_id = "null"
				# u_name = "null"
				u_location = "null"
				# u_followerscount = 0
				# u_friendscount = 0
				# u_createdate = "null"
		elif ka == "entities":
			e_count = 0
			e_text = []
			if va is not None:
				for kb,vb in va.iteritems():
					if kb == "hashtags":
						if vb is not None:
							for x in vb:
								for kc, vc in x.iteritems():
									if kc == "text":
										e_count += 1
										e_text.append(vc.replace("\n", "").lower())

			# HASH RELATED ONLY AND REMOVE IF NOT RELATED
			found = False
			for text in e_text:
				if text in notallowedhash:
					return -1
				if text in allowedhash:
					found = True
			if not found:
				return -1
	
	outvalue = str(t_id) + ","
	outvalue += t_createdate + ","
	outvalue += t_text.replace(",","_").replace("\n"," ") + ","
	# outvalue += str(t_coordinates).replace(",","-") + ","
	# outvalue += t_place + ","
	# outvalue += str(t_favoritecount) + ","
	# outvalue += str(t_retweetcount) + ","
	# outvalue += t_lang + ","
	# outvalue += str(u_id) + ","
	# outvalue += u_name.replace(",","_") + ","
	
	if t_place is not None and t_place != "null" and t_place != "" and t_place != " ":
		try:
			temp = Location2Country(t_place)
			if temp is not None and temp != "null" and temp != "" and temp != " ":
				outvalue += temp + ","
		except Exception,e:
			outvalue += "null,"
	 
	elif u_location is not None and u_location != "null" and u_location != "" and u_location != " ":
		try:
			temp = Location2Country(u_location)
			if temp is not None and temp != "null" and temp != "" and temp != " ":
				outvalue += temp + ","
		except Exception,e:
			outvalue += "null,"
	else:
		outvalue += "null," 
	
	# outvalue += str(u_followerscount) + ","
	# outvalue += str(u_friendscount) + ","
	# outvalue += u_createdate + ","
	outvalue += str(e_count)
	if e_count > 0:
		outvalue += ","
		for i in range(0, e_count):
			if i == 0:
				outvalue += e_text[i]
			else:
				outvalue += "+" + e_text[i]
	else:
		outvalue += ",null"

	return outvalue.replace(",,",",null,")

rootdir5 = "/home/masdarcis/Documents/projects_amalfi/twitter_data/programs/codes/05"
rootdir4 = "/home/masdarcis/Documents/projects_amalfi/twitter_data/programs/codes/04"
dirs5 = [["26","27","28","29","30","01","02"],
["03","04","05","06","07","08","09"],
["10","11","12","13","14","15","16"],
["17","18","19","20","21","22","23"],
["24","25","26","27","28","29","30"]]

filehash = open("hashtag.list","r")
allowedhash = []
for hashline in filehash:
	allowedhash.append(hashline.replace("\n","").lower())
filehash.close()

# LOAD NOT HASHTAG LIST
filehash = open("nothashtag.list","r")
notallowedhash = []
for hashline in filehash:
	notallowedhash.append(hashline.replace("\n","").lower())
filehash.close()

print "Processing May!!!"
count = 1
errordir = rootdir5 + "/errorfile.error"
errorfile = open(errordir, "w")
outputdir = rootdir5 + "/result.csv"
outputfile = open(outputdir, "w+")

for week in dirs5:
	print "Processing week " + str(count) + "..."
	for date in week:
		if (date == "26" or date == "27" or date == "28" or date == "29" or date == "30") and count == 1:
			currentdir = rootdir4 + "/" + date
		else:
			currentdir = rootdir5 + "/" + date

		print "Processing date : " + date + "... NOW" 
		filesindir = list_files(currentdir)
		
		progress = 1
		if len(filesindir) > 0:
			for file in sorted(filesindir):
				print progress, " out of ", len(filesindir), " from date : ", date 
				filename, fileextension = os.path.splitext(file)
				try:
					untarbz2(file, filename)
				except Exception, e:
					print "Error in untaring : ", file, "--", str(e)
					errorfile.write("Error in file : " + file)
					errorfile.write(os.linesep)
					continue

				# OPERATION
				fileread = open(filename, "r")
				line = fileread.readline()
				
				while line:
					try:
						towrite = _jsontocsv(line, allowedhash, notallowedhash)

						if towrite != -1:
							print "In at : ", file
							outputfile.write(towrite.encode('ascii','ignore').replace("  ",""))
							outputfile.write("," + str(count))
							outputfile.write(os.linesep)
						line = fileread.readline()

					except Exception,e:
						print "Error in csving : ", str(e)
						errorfile.write("Error in csving : " + str(e) + "--" + line)
						errorfile.write(os.linesep)
						line = fileread.readline()
						continue

				fileread.close()
				os.remove(filename)

				outputfile.flush()
				errorfile.flush()
				progress += 1

	count = count + 1

outputfile.close()
errorfile.close()
print "Preprocessing Finished!"