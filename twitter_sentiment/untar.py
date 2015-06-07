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

filenames = ["archiveteam-twitter-stream-2014-02.tar", "archiveteam-twitter-stream-2014-03.tar", "archiveteam-twitter-stream-2014-04.tar", "archiveteam-twitter-stream-2014-05.tar"]
for value in filenames:
	try:
		untar(value)
	except:
		print "Something wrong in untar-ing : ", value