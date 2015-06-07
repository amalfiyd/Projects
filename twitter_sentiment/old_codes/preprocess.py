import bz2, os, math, json, subprocess, sys

# DA UNTARER
def untarbz2(basefile, outfile):
	tar = bz2.BZ2File(basefile)
	data = tar.read()
	filez = open(outfile, 'wb')
	filez.write(data)
	filez.close()

# DA FILE ITERATOR
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

# INTEGER HELPER
def inthelper(input):
	if input < 10:
		return "0" + str(input)
	else:
		return str(input)

# JSON TO CSV RETURN STRING
def _jsontocsv(jsoninput, allowedhash, notallowedhash):

	# The conversion algorithm
	obj = json.loads(jsoninput)
	outvalue = None

	t_id = None
	t_createdate = None
	t_text = None
	t_coordinates = None
	t_place = None
	# t_favoritecount = None
	# t_retweetcount = None
	# t_lang = None
	# u_id = None
	u_name = None
	u_location = None
	# u_followerscount = None
	# u_friendscount = None
	# u_createdate = None
	e_count = None
	e_text = None

	for ka, va in obj.iteritems():
		if ka == "delete":
			return -1
		elif ka == "id":
			t_id = va
		elif ka == "created_at":
			t_createdate = va
		elif ka == "text":
			# CLEAN FROM NOT ALLOWED HASH
			for notokay in notallowedhash:
				if notokay in va.lower():
					return -1 
			t_text = va
		elif ka == "coordinates":
			if va is not None:
				for kb, vb in va.iteritems():
					if kb == "coordinates":
						t_coordinates = vb
						break
			else:
				t_coordinates = "null"
		elif ka == "place":
			if va is not None:
				for kb, vb in va.iteritems():
					if kb == "country_code":
						t_place = vb
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
					if kb == "name":
						u_name = vb
						break
					elif kb == "location":
						u_location = vb
					# elif kb == "followers_count":
					# 	u_followerscount = vb
					# elif kb == "friends_count":
					# 	u_friendscount = vb
					# elif kb == "created_at":
					# 	u_createdate = vb
			else:
				# u_id = "null"
				u_name = "null"
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
										e_text.append(vc)

			# HASH RELATED ONLY AND REMOVE IF NOT RELATED
			found = False
			for text in e_text:
				temp = text.replace("\n","").lower()
				if temp in notallowedhash:
					return -1
				if temp in allowedhash:
					found = True
			if not found:
				return -1
	
	outvalue = str(t_id) + ","
	outvalue += t_createdate + ","
	outvalue += t_text.replace(",","_") + ","
	outvalue += str(t_coordinates).replace(",","-") + ","
	outvalue += t_place + ","
	# outvalue += str(t_favoritecount) + ","
	# outvalue += str(t_retweetcount) + ","
	# outvalue += t_lang + ","
	# outvalue += str(u_id) + ","
	outvalue += u_name.replace(",","_") + ","
	# outvalue += u_location.replace(", ","-") + ","
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

	return outvalue.replace("\n"," ").replace(",,",",?,")

# FEBRUARY
rootdir2 = "/home/masdarcis/Documents/projects_amalfi/twitter_data/collected/new/codes/02"
dirs2 = [["01","02","03","04","05","06","07"],
["08","09","10","11","12","13","14"],
["15","16","17","18","19","20","21"],
["22","23","24","25","26","27","28"]]

# MARCH
rootdir3 = "/home/masdarcis/Documents/projects_amalfi/twitter_data/collected/new/codes/03"
dirs3 = [["01","02","03","04","05","06","07"],
["08","09","10","11","12","13","14"],
["15","16","17","18","19","20","21"],
["22","23","24","25","26","27","28"]]

# APRIL
rootdir4 = "/home/masdarcis/Documents/projects_amalfi/twitter_data/collected/new/codes/04"
dirs4 = [["29","30","31","01","02","03","04"],
["05","06","07","08","09","10","11"],
["12","13","14","15","16","17","18"],
["19","20","21","22","23","24","25"]]

# MAY
rootdir5 = "/home/masdarcis/Documents/projects_amalfi/twitter_data/collected/new/codes/05"
dirs5 = [["24","25","26","27","28","29","30"]]
# ["17","18","19","20","21","22","23"]

# LOAD HASHTAG LIST
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

# MARCH, FEB PROCESSING
# print "Processing March!!!"
# count = 4
# errordir = rootdir3 + "/error.file"
# errorfile = open(errordir, "w+")
# for week in dirs3:
# 	print "Processing week " + str(count) + "..."

# 	outputdir = rootdir3 + "/week" + str(count) + "_22.csv"
# 	outputfile = open(outputdir, "w+")
# 	for date in week:
# 		print "Processing date : " + date + "... NOW" 
# 		currentdir = rootdir3 + "/" + date
# 		filesindir = list_files(currentdir)

# 		progress = 1
# 		if len(filesindir) > 0:
# 			for file in filesindir:
# 				print progress, " out of ", len(filesindir), " from date : ", date 
# 				filename, fileextension = os.path.splitext(file)
# 				try:	
# 					untarbz2(file, filename)

# 					# OPERATION
# 					fileread = open(filename, "r")
# 					line = fileread.readline()
					
# 					while line:
# 						towrite = _jsontocsv(line, allowedhash, notallowedhash)
# 						if towrite != -1:
# 							outputfile.write(towrite.encode("utf8"))
# 							outputfile.write(os.linesep)
						
# 						line = fileread.readline()

# 					fileread.close()
# 					os.remove(filename)

# 				except:
# 					errorfile.write("Error in file : " + file + " ")
# 					errorfile.write(os.linesep)

# 				progress += 1

# 	count = count + 1
# 	outputfile.close()

# errorfile.close()

# APRIL PROCESSING 
# print "Processing April!!!"
# count = 1
# errordir = rootdir4 + "/error.file"
# errorfile = open(errordir, "w+")
# for week in dirs4:
# 	print "Processing week " + str(count) + "..."

	# outputdir = ""
	# outputfile = None
	# for date in week:
	# 	if outputfile is None:
	# 		outputdir = rootdir4 + "/week" + str(count) + ".csv"
	# 		outputfile = open(outputdir, "w+")

	# 	if (date == "29" or date == "30" or date == "31") and count == 1:
	# 		currentdir = rootdir3 + "/" + date
	# 	else:
	# 		currentdir = rootdir4 + "/" + date

	# 	print "Processing date : " + date + "... NOW" 
	# 	filesindir = list_files(currentdir)
		
# 		progress = 1
# 		if len(filesindir) > 0:
# 			for file in filesindir:
# 				print progress, " out of ", len(filesindir), " from date : ", date 
# 				filename, fileextension = os.path.splitext(file)
# 				try:
# 					untarbz2(file, filename)

# 					# OPERATION
# 					fileread = open(filename, "r")
# 					line = fileread.readline()
					
# 					while line:
# 						towrite = _jsontocsv(line, allowedhash, notallowedhash)
# 						if towrite != -1:
# 							outputfile.write(towrite.encode("utf8"))
# 							outputfile.write(os.linesep)
						
# 						line = fileread.readline()

# 					fileread.close()
# 					os.remove(filename)

# 				except:
# 					errorfile.write("Error in file : " + file)
# 					errorfile.write(os.linesep)

# 				progress += 1

# 	count = count + 1
# 	outputfile.close()

# errorfile.close()

# MAY PROCESSING
print "Processing May!!!"
count = 5
errordir = rootdir5 + "/error.file"
errorfile = open(errordir, "w+")
for week in dirs5:
	print "Processing week " + str(count) + "..."

	outputdir = ""
	outputfile = None
	for date in week:
		
		if outputfile is None:
			outputdir = rootdir5 + "/week" + str(count) + ".csv"
			outputfile = open(outputdir, "w+")

		if (date == "26" or date == "27" or date == "28" or date == "29" or date == "30") and count == 1:
			outputdir = rootdir5 + "/week" + str(count) + ".csv"
			outputfile = open(outputdir, "w+")
			currentdir = rootdir4 + "/" + date
		else:
			outputdir = rootdir5 + "/week" + str(count) + ".csv"
			outputfile = open(outputdir, "w+")
			currentdir = rootdir5 + "/" + date

		print "Processing date : " + date + "... NOW" 
		filesindir = list_files(currentdir)
		
		progress = 1
		if len(filesindir) > 0:
			for file in filesindir:
				print progress, " out of ", len(filesindir), " from date : ", date 
				filename, fileextension = os.path.splitext(file)
				untarbz2(file, filename)

				# OPERATION
				fileread = open(filename, "r")
				line = fileread.readline()
				
				while line:
					towrite = _jsontocsv(line, allowedhash, notallowedhash)
					if towrite != -1:
						outputfile.write(towrite.encode("utf8"))
						outputfile.write(os.linesep)
					
					line = fileread.readline()

				fileread.close()
				os.remove(filename)

				progress += 1

	count = count + 1
	outputfile.close()

print "Preprocessing Finished!"
# subprocess.call(["sudo", "shutdown", "-h", "now"])