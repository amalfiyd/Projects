import json

# JSON converter for 1 tweet
def _jsontocsv(jsoninput):
	obj = json.loads(jsoninput)
	outvalue = None

	t_id = None
	t_createdate = None
	t_text = None
	t_coordinates = None
	t_place = None
	t_favoritecount = None
	t_retweetcount = None
	t_lang = None
	u_id = None
	u_name = None
	u_location = None
	u_followerscount = None
	u_friendscount = None
	u_createdate = None
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
		elif ka == "favorite_count":
			t_favoritecount = va
		elif ka == "retweet_count":
			t_retweetcount = va
		elif ka == "lang":
			t_lang = va
		elif ka == "user":
			if va is not None:
				for kb, vb in va.iteritems():
					if kb == "id":
						u_id = vb
					elif kb == "name":
						u_name = vb
					elif kb == "location":
						u_location = vb
					elif kb == "followers_count":
						u_followerscount = vb
					elif kb == "friends_count":
						u_friendscount = vb
					elif kb == "created_at":
						u_createdate = vb
			else:
				u_id = "null"
				u_name = "null"
				u_location = "null"
				u_followerscount = 0
				u_friendscount = 0
				u_createdate = "null"
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
	
	outvalue = str(t_id) + ","
	outvalue += t_createdate + ","
	outvalue += t_text.replace(",","_") + ","
	outvalue += str(t_coordinates).replace(",","-") + ","
	outvalue += t_place + ","
	outvalue += str(t_favoritecount) + ","
	outvalue += str(t_retweetcount) + ","
	outvalue += t_lang + ","
	outvalue += str(u_id) + ","
	outvalue += u_name.replace(",","_") + ","
	# outvalue += u_location.replace(", ","-") + ","
	outvalue += str(u_followerscount) + ","
	outvalue += str(u_friendscount) + ","
	outvalue += u_createdate + ","
	outvalue += str(e_count)
	if e_count > 0:
		for i in range(0, e_count):
			outvalue += "+" + e_text[i]
	else:
		outvalue += ",null"

	return outvalue.replace("\n"," ").replace(",,",",?,")