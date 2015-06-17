#!/usr/bin/python
# -*- coding: utf-8 -*-

import MySQLdb as mdb
import sys
import math
from collections import Counter

try:
    con = mdb.connect('localhost', 'root', 'masdarcis1234', 'credbank')
    con.autocommit(True)
    cur = con.cursor()
    cur.execute("SELECT * FROM topic_ratings")

    rows = cur.fetchall()
    iters = 1
    for row in rows:
    	le_id = row[0]
    	ratings = row[5].split("#")
    	ratings = map(lambda x : int(x), ratings)
    	c = Counter(ratings)
    	n_2s = c.most_common()[0]
        percentage = n_2s[1] / float(sum(x[1] for x in c.most_common()))
        out_val = math.floor(percentage*10)/10

        temp1 = "UPDATE topic_ratings SET threshold_group = "
        temp2 = str(out_val)
        temp3 = " WHERE id = "
        temp4 = str(le_id)

        temp = []
        temp.append(temp1)
        temp.append(temp2)
        temp.append(temp3)
        temp.append(temp4)
        sql = "".join(temp)

        cur.execute(sql)

    	# if iters == 2: 	
    	# 	break
    	print iters
    	iters = iters + 1
    	
except mdb.Error, e:
  
    print "Error %d: %s" % (e.args[0],e.args[1])
    sys.exit(1)
    
finally:    
        
    if con:    
        con.close()