import pickle as pck
import re
import pandas as pd
from textblob import TextBlob

basedir = "/media/masdarcis/d85e693b-e31c-4c51-8ce9-bcfaad97b9ba/oil_price/"
filename = "op_stream_Mon_Jun_22_17:54:00_2015.pkl"
check = pck.load(open(basedir + filename, "rb"))

data = []
data.append(["text", "lang", "polarity", "subjectivity"])
for row in check:
	data.append([row['text'], row['lang'], 0.0, 0.0])

df = pd.DataFrame(data[1:], columns=data[0])
tb = [TextBlob(x) for x in df['text']]
df['polarity'] = [x.sentiment.polarity for x in tb]
df['subjectivity'] = [x.sentiment.subjectivity for x in tb]

test = df[df['lang'] == "en"]