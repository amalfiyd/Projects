import matplotlib.pyplot as plt
import MySQLdb as mdb
import sys

try:
    con = mdb.connect('localhost', 'root', 'masdarcis1234', 'credbank')
    cur = con.cursor()
    cur.execute("SELECT * FROM temp2")

    rows = cur.fetchall()
    my_dict = {} 
    my_dict['0.1'] = []
    my_dict['0.2'] = []
    my_dict['0.3'] = []
    my_dict['1.0'] = []

    for row in rows :
        if row[2] == 0.1 :
            my_dict['0.1'].append(row[1])
        elif row[2] == 0.2 :
            my_dict['0.2'].append(row[1])
        elif row[2] == 0.3 :
            my_dict['0.3'].append(row[1])
        elif row[2] == 1.0 :
            my_dict['1.0'].append(row[1])
    
    group1 = my_dict['0.1']
    group2 = my_dict['0.2']
    group3 = my_dict['0.3']
    group10 = my_dict['1.0']
    
    final_values = []
    final_axes = ['0.1','0.2','0.3','1.0']

    group1_avg = []
    for x in range(1, len(group1)):
        growth = (group1[x] - group1[x-1]) / group1[x-1]
        group1_avg.append(growth)
    final_values.append(sum(group1_avg) / len(group1_avg))

    group2_avg = []
    for x in range(1, len(group2)):
        growth = (group2[x] - group2[x-1]) / group2[x-1]
        group2_avg.append(growth)
    final_values.append(sum(group2_avg) / len(group2))

    group3_avg = []
    for x in range(1, len(group3)):
        growth = (group3[x] - group3[x-1]) / group3[x-1]
        group3_avg.append(growth)
    final_values.append(sum(group3_avg) / len(group3))

    group10_avg = []
    for x in range(1, len(group10)):
        growth = (group10[x] - group10[x-1]) / group10[x-1]
        group10_avg.append(growth)
    final_values.append(sum(group10_avg) / len(group10))

    # average_growth = sum(count_values) / len(count_values)
    # print "Average Growth : ", average_growth 
    plt.plot(final_axes,final_values)
    plt.ylabel("Growth Rate")
    plt.xlabel("Percentage on -2 as Ratings")
    plt.gcf().canvas.set_window_title("Correlation b/w Growth & Uncredibility")
    plt.show()
    	
except mdb.Error, e:
  
    print "Error %d: %s" % (e.args[0],e.args[1])
    sys.exit(1)
    
finally:    
        
    if con:    
        con.close()