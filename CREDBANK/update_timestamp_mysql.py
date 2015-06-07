#!/usr/bin/python
# -*- coding: utf-8 -*-

import MySQLdb as mdb
import sys
from collections import Counter

try:
    con = mdb.connect('localhost', 'root', 'masdarcis1234', 'credbank')
    con.autocommit(True)
    cur = con.cursor()
    cur.execute("SELECT * FROM topic_tweets")

    rows = cur.fetchall()
    iters = 1
    for row in rows:
    	le_id = row[0]
    	field = row[1].split("_")[2].split("-")[1]

        temp1 = "UPDATE topic_tweets SET timestamp = "
    	temp2 = field
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