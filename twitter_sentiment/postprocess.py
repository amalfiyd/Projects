import re
import os

# # FEBRUARY
# file = open("preprocessed/feb_set.csv","r")
# fileout = open("preprocessed/feb_set2.csv","w")

# line = file.readline()
# while line:
# 	temp = line.split(",")
# 	try:
# 		test = int(temp[3])

# 		# Processing
# 		string = temp[0]
# 		string += "," + temp[1]
# 		string += "," + temp[2]
# 		string += ",null," + temp[3]
# 		string += "," + temp[4]
# 		string += "," + temp[5]
		
# 		fileout.write(string)

# 		line = file.readline()
# 	except ValueError:
# 		# Processing
# 		string = temp[0]
# 		string += "," + temp[1]
# 		string += "," + temp[2]
# 		string += "," + temp[3]
# 		string += "," + temp[4]
# 		string += "," + temp[5]
# 		string += "," + temp[6]

# 		fileout.write(string)

# 		line = file.readline()

# file.close()
# fileout.close()

# # MARCH
# file = open("preprocessed/mar_set.csv","r")
# fileout = open("preprocessed/mar_set2.csv","w")

# line = file.readline()
# while line:
# 	temp = line.split(",")
# 	print temp
# 	try:
# 		test = int(temp[3])

# 		# Processing
# 		string = temp[0]
# 		string += "," + temp[1]
# 		string += "," + temp[2]
# 		string += ",null," + temp[3]
# 		string += "," + temp[4]
# 		string += "," + temp[5]
		
# 		fileout.write(string)

# 		line = file.readline()
# 	except ValueError:
# 		# Processing
# 		string = temp[0]
# 		string += "," + temp[1]
# 		string += "," + temp[2]
# 		string += "," + temp[3]
# 		string += "," + temp[4]
# 		string += "," + temp[5]
# 		string += "," + temp[6]

# 		fileout.write(string)

# 		line = file.readline()

# file.close()
# fileout.close()

# # APRIL
# file = open("preprocessed/apr_set.csv","r")
# fileout = open("preprocessed/apr_set2.csv","w")

# line = file.readline()
# while line:
# 	temp = line.split(",")
# 	print temp
# 	try:
# 		test = int(temp[3])

# 		# Processing
# 		string = temp[0]
# 		string += "," + temp[1]
# 		string += "," + temp[2]
# 		string += ",null," + temp[3]
# 		string += "," + temp[4]
# 		string += "," + temp[5]
		
# 		fileout.write(string)

# 		line = file.readline()
# 	except ValueError:
# 		# Processing
# 		string = temp[0]
# 		string += "," + temp[1]
# 		string += "," + temp[2]
# 		string += "," + temp[3]
# 		string += "," + temp[4]
# 		string += "," + temp[5]
# 		string += "," + temp[6]

# 		fileout.write(string)

# 		line = file.readline()

# file.close()
# fileout.close()

# # MAY
file = open("preprocessed/may_set.csv","r")
fileout = open("preprocessed/may_set2.csv","w")

line = file.readline()
while line:
	temp = line.split(",")
	print temp
	try:
		test = int(temp[3])

		# Processing
		string = temp[0]
		string += "," + temp[1]
		string += "," + temp[2]
		string += ",null," + temp[3]
		string += "," + temp[4]
		string += "," + temp[5]
		
		fileout.write(string)

		line = file.readline()
	except ValueError:
		# Processing
		string = temp[0]
		string += "," + temp[1]
		string += "," + temp[2]
		string += "," + temp[3]
		string += "," + temp[4]
		string += "," + temp[5]
		string += "," + temp[6]

		fileout.write(string)

		line = file.readline()

file.close()
fileout.close()