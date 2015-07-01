import tarfile, sys

def untar(filename):
	if(filename.endswith(".tar")):
		print "Processing : ", filename, "..."
		tar = tarfile.open(filename)
		tar.extractall()
		tar.close()
		print "Extract : ", filename, "is done!"
	else:
		print filename, " is not a .tar file!"

basedir = "/media/masdarcis/6bd2f6a3-27d0-487b-a810-74aebfeff2c6/"
filename = "archiveteam-twitter-stream-2014-06.tar"
try:
	untar(basedir + filename)
except:
	print "Something wrong in untar-ing : ", value