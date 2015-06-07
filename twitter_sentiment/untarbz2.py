import bz2
import os

def untar(filename):
	tar = bz2.BZ2File(filename)
	data = tar.read()
	newfilepath = os.path.splitext(filename)[0]
	open(newfilepath, 'wb').write(data)
	# for tarinfo in tar:
	# 	if tarinfo.isreg():
	# 		f = tar.extractfile(tarinfo)

untar("23.json.bz2")

# for filename in glob.glob("*.bz2"):
# 	print filename