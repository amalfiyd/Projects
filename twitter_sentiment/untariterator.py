import os
import bz2

# Our main function for unzipping
def untar(basefile, outfile):
	tar = bz2.BZ2File(basefile)
	data = tar.read()
	filez = open(outfile, 'wb')
	filez.write(data)
	filez.close()

# Da file iterator
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

# the main process function
print "Ubz2ing currently on process..."

rootdir = "/home/masdarcis/Documents/projects_amalfi/twitter_data/collected/02"

total = 0
for subdir, dirs, files in os.walk(rootdir):
	for file in files:
		if file.endswith(".bz2"):
			total = total+1

print "Total : ", total

# Get list of filenames
listoffilename = list_files(rootdir)
count = 1

for filename in listoffilename:
	print "Processing : ", filename, " ", count, " out of ", total
	
	tempstring = filename.split("/")
	tempstring2 = tempstring[len(tempstring)-1].split(".")
	directory = ""
	for i in range(0, 7):
		directory = directory + tempstring[i] + "/"
	directory = directory + "unzipped/" + tempstring[7] + "/"
	outindex = tempstring[7] + "-" + tempstring[8] + "_" + tempstring[9] + ":" + tempstring2[0]
	extension = tempstring2[1]
	outfile = directory + outindex + "." + extension
	untar(filename, outfile)
	
	count = count + 1

print "IT IS DONE!!!"