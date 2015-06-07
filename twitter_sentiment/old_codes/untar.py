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

filenames = ["../feb14.tar", "../mar14.tar", "../apr14.tar", "../may14.tar"]
for value in filenames:
	try:
		untar(value)
	except:
		print "Something wrong in untar-ing : ", value