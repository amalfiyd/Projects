import jsontocsv
import os

# create CSV file after parsing

rootdir = "/home/aydarusman/Documents/Conference Stuff/old"
outdir = "/home/aydarusman/Documents/Conference Stuff/old/test.csv"
outfile = open(outdir, "w")

print "Converting to csv file process started..."
for root, dirs, files in os.walk("."):
	for file in files:
		if file.endswith(".json"):
			thefile = open(file)
			line = thefile.readline()

			while line:
				# try:
				towrite = jsontocsv._jsontocsv(line)
				if towrite != -1:
					outfile.write(towrite.encode("utf8"))
					outfile.write(os.linesep)
				# except Exception as exp:
				# 	print exp.args
				# 	break
				line = thefile.readline()

			thefile.close()

outfile.close()
print "Converting to csv file process finished :)"