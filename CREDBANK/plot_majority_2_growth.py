import matplotlib.pyplot as plt
import MySQLdb as mdb
import sys

try:
    con = mdb.connect('localhost', 'root', 'masdarcis1234', 'credbank')
    con.autocommit(True)
    cur = con.cursor()
    cur.execute("SELECT * FROM majority_turkratings_2_preprocessed")

    rows = cur.fetchall()
    iters = 1
    week_labels = []
    count_values = []
    past_count = rows[0][3]
    past_label = rows[0][0]
    for row in rows[1:]:
    	temp_label = "" + str(past_label) + "-" + str(row[0])
    	temp_value = (row[3] - past_count) / past_count

    	past_label = row[0]
    	past_count = row[3]

    	week_labels.append(temp_label)
    	count_values.append(temp_value)

    	# # if iters == 2: 	
    	# # 	break
    	# print iters
    	# iters = iters + 1
    	# break

    # print week_labels
    # print count_values
    average_growth = sum(count_values) / len(count_values)
    print "Average Growth : ", average_growth 
    plt.plot(range(0, len(week_labels)),count_values)
    plt.ylabel("Growth Rate")
    plt.xlabel("Weekly Time Series")
    plt.gcf().canvas.set_window_title("TurkRatings w/ Majority 2")
    plt.show()
    	
except mdb.Error, e:
  
    print "Error %d: %s" % (e.args[0],e.args[1])
    sys.exit(1)
    
finally:    
        
    if con:    
        con.close()