import os
import json
import bz2

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

def process_date(instring):
	splitted = instring.split(" ")
	mon_val = convert_month(splitted[1]) 
	date_val = splitted[2]
	year_val = splitted[5]
	return date_val + "-" + mon_val + "-" + year_val

def convert_month(monstring):
	my_tuple = {"jan":"01", "feb":"02", "mar":"03", "apr":"04", "may":"05", "jun":"06", "jul":"07", "aug":"08", "sep":"09", "oct":"10", "nov":"11", "dec":"12"}
	return my_tuple[monstring.lower()]

def json_to_csv(line):
	obj = json.loads(line)
	outvalue = None

	t_id = None
	t_createdate = None
	t_text = None
	t_place = None
	u_id = None
	u_name = None
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
			t_text = va
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
		elif ka == "lang":
			if va != "en":
				return -1
		elif ka == "user":
			if va is not None:
				for kb, vb in va.iteritems():
					if kb == "id":
						u_id = vb
					elif kb == "name":
						u_name = vb
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

	# print t_id
	# print process_date(t_createdate) 
	# print t_text
	# print t_place
	# print u_id
	# print u_name
	# print e_count
	# print e_text

	outvalue = []
	outvalue.append(str(t_id))
	outvalue.append(process_date(t_createdate))
	outvalue.append(t_text.replace(",","_").replace("\n"," "))
	outvalue.append(str(u_id))
	outvalue.append(u_name)
	outvalue.append(str(e_count))
	if e_count > 0:
		outvalue.append("#".join(e_text))
	else:
		outvalue.append("--NA--")

	return ",".join(outvalue)


# -------------------------
# ----- MAIN FUNCTION -----
# -------------------------
base_dir = "/home/masdarcis/Projects/dataset/twitter_febtomay14/04"
files = sorted(list_files(base_dir))
out_dir = "/home/masdarcis/Projects/dataset/twitter_febtomay14/apr14_data.csv"
filewrite = open(out_dir, "w")

count_files = len(files)
iter_files = 1
for le_file in files:
	print "Processing Files : " + str(iter_files) + " / " + str(count_files)
	iter_files = iter_files + 1
	try :
		filename, fileext = os.path.splitext(le_file)
		untarbz2(le_file, filename)

		fileread = open(filename,"r")

		# lines = sum(1 for line in open(filename, "r"))
		# iter_lines = 1
		for line in fileread:
			# print "Processing " + str(iter_lines) + " / " + str(lines)
			# iter_lines = iter_lines + 1
			to_write = json_to_csv(line)
			if to_write != -1:
				filewrite.write(to_write.encode('ascii', 'ignore'))
				filewrite.write("\n")

		fileread.close()

	except Exception, e:
		print "Error : ", e
		continue

filewrite.close()