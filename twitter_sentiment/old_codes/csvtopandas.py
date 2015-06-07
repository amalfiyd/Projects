import os
import pandas
# the code is still shitty

def maxcounter(filename):
	file = open(filename, "r")
	maxcount = 0
	for line in file:
		temp = line.split(",")
		if maxcount < len(temp):
			maxcount = len(temp)
	file.close()
	return maxcount

def addfollowingvalues(maxcount, filename):
	file = open(filename, "r")
	out_lines = []
	for line in file:
		line = line.replace("\n","")
		line_values = line.split(",")
		out_values = line_values
		if maxcount > len(line_values):
			diff = maxcount - len(line_values)
			for i in range(0, diff):
				out_values.append("null")
			out_lines.append(out_values)
	
	file.close()
	file = open("test2.csv", "w")

	for i in out_lines:
		if i[7] == "en":
			for j in range(0, len(i)):
				file.write(i[j])
				if j < len(i)-1:
					file.write(",")
			file.write("\n")
	file.close()

maxcount = maxcounter("test.csv")
addfollowingvalues(maxcount, "test.csv")

temp = pandas.read_csv("test2.csv")
print temp
# temp = open("test2.csv","r")
# for line in temp:
# 	temp2 = line.split(",")
# 	print len(temp2)
# temp.close()