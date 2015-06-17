import matplotlib.pyplot as plt
import MySQLdb as mdb
import sys

try:
    con = mdb.connect('localhost', 'root', 'masdarcis1234', 'credbank')
    cur = con.cursor()
    cur.execute("SELECT * FROM temp")

    rows = cur.fetchall()
    my_dict = {} 
    key = float(0.3)
    end_key = float(1.0)
    while key <= end_key:
        my_dict[str(key)] = []
        key = key + float(0.1)

    for row in rows :
        if row[2] == 0.3 :
            my_dict['0.3'].append(row[1])
        elif row[2] == 0.4 :
            my_dict['0.4'].append(row[1])
        elif row[2] == 0.5 :
            my_dict['0.5'].append(row[1])
        elif row[2] == 0.6 :
            my_dict['0.6'].append(row[1])
        elif row[2] == 0.7 :
            my_dict['0.7'].append(row[1])
        elif row[2] == 0.8 :
            my_dict['0.8'].append(row[1])
        elif row[2] == 0.9 :
            my_dict['0.9'].append(row[1])
        elif row[2] == 1.0 :
            my_dict['1.0'].append(row[1])
    
    group3 = my_dict['0.3']
    group4 = my_dict['0.4']
    group5 = my_dict['0.5']
    group6 = my_dict['0.6']
    group7 = my_dict['0.7']
    group8 = my_dict['0.8']
    group9 = my_dict['0.9']
    group10 = my_dict['1.0']

    final_values = []
    final_axes = ['0.5','0.6','0.7','0.8','0.9','1.0']

    # group3_avg = []
    # for x in range(1, len(group3)):
    #     growth = (group3[x] - group3[x-1]) / group3[x-1]
    #     group3_avg.append(growth)
    # final_values.append(sum(group3_avg) / len(group3_avg))

    # group4_avg = []
    # for x in range(1, len(group4)):
    #     growth = (group4[x] - group4[x-1]) / group4[x-1]
    #     group4_avg.append(growth)
    # final_values.append(sum(group4_avg) / len(group4))

    group5_avg = []
    for x in range(1, len(group4)):
        growth = (group5[x] - group5[x-1]) / group5[x-1]
        group5_avg.append(growth)
    final_values.append(sum(group5_avg) / len(group5))

    group6_avg = []
    for x in range(1, len(group6)):
        growth = (group6[x] - group6[x-1]) / group6[x-1]
        group6_avg.append(growth)
    final_values.append(sum(group6_avg) / len(group6))

    group7_avg = []
    for x in range(1, len(group7)):
        growth = (group7[x] - group7[x-1]) / group7[x-1]
        group7_avg.append(growth)
    final_values.append(sum(group7_avg) / len(group7))

    group8_avg = []
    for x in range(1, len(group8)):
        growth = (group8[x] - group8[x-1]) / group8[x-1]
        group8_avg.append(growth)
    final_values.append(sum(group8_avg) / len(group8))

    group9_avg = []
    for x in range(1, len(group9)):
        growth = (group9[x] - group9[x-1]) / group9[x-1]
        group9_avg.append(growth)
    final_values.append(sum(group9_avg) / len(group9))

    group10_avg = []
    for x in range(1, len(group10)):
        growth = (group10[x] - group10[x-1]) / group10[x-1]
        group10_avg.append(growth)
    final_values.append(sum(group10_avg) / len(group10))

    # average_growth = sum(count_values) / len(count_values)
    # print "Average Growth : ", average_growth 
    plt.plot(final_axes,final_values)
    plt.ylabel("Growth Rate")
    plt.xlabel("Percentage on 2 as Ratings")
    plt.gcf().canvas.set_window_title("Correlation b/w Growth & Credibility")
    plt.show()
    	
except mdb.Error, e:
  
    print "Error %d: %s" % (e.args[0],e.args[1])
    sys.exit(1)
    
finally:    
        
    if con:    
        con.close()