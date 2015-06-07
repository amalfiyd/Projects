import matplotlib.pyplot as pyplot
import csv

x = []
y = []

with open("result.csv","r") as csvfile:
	result = csv.reader(csvfile, delimiter=',', quotechar='"')
	for row in result :
		x.append(row[0])
		y.append(row[1])

pyplot.plot(x,y, 'bo');
pyplot.show()