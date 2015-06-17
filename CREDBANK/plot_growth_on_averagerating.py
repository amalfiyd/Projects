import matplotlib.pyplot as plt
import MySQLdb as mdb
import sys

try:
    con = mdb.connect('localhost', 'root', 'masdarcis1234', 'credbank')
    cur = con.cursor()
    cur.execute("SELECT * FROM temp3")

    rows = cur.fetchall()
    # final_values = []
    # final_axes = ['0.5','0.6','0.7','0.8','0.9','1.0']
    count_dict = {}
    final_dict = {}

    for i in range(2,len(rows)):
        if str(rows[i][2]) not in count_dict.keys():
            count_dict[str(rows[i][2])] = []
            final_dict[str(rows[i][2])] = 0

    for i in range(2,len(rows)):
        if rows[i-1][2] != rows[i][2]:
            continue
        else:
            count_dict[str(rows[i][2])].append((rows[i][1] - rows[i-1][1]) / rows[i-1][1])
    
    for i in final_dict.keys():
        final_dict[i] = sum(count_dict[i]) / len(count_dict[i])

    final_values = []
    final_labels = []
    for i in sorted(final_dict.keys()):
        final_labels.append(i)
        final_values.append(final_dict[i])

    print final_values
    print final_labels

    # average_growth = sum(count_values) / len(count_values)
    # print "Average Growth : ", average_growth 
    plt.plot(final_labels,final_values)
    plt.ylabel("Growth Rate")
    plt.xlabel("Average Ratings on Particular Topic")
    plt.gcf().canvas.set_window_title("Correlation b/w Growth & Credibility")
    plt.show()
    	
except mdb.Error, e:
  
    print "Error %d: %s" % (e.args[0],e.args[1])
    sys.exit(1)
    
finally:    
        
    if con:    
        con.close()