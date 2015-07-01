from twython import Twython,TwythonStreamer
import pickle,time,re

result=[]

class MyStreamer(TwythonStreamer):
       
    def on_success(self, data):
        global result
        if 'text' in data:
            print "Result entry #"+str(len(result))+" "+data['text'].encode('utf-8')
            result.append(data)
            if len(result)>1000:
                filetag=re.sub("\s","_",time.ctime())
                pickle.dump(result,open("/media/masdarcis/d85e693b-e31c-4c51-8ce9-bcfaad97b9ba/oil_price/op_stream_"+filetag+".pkl","w+"))
                result=[]
                
    def on_error(self, status_code, data):
        print status_code
        
        # Want to stop trying to get data because of the error?
        # Uncomment the next line!
        self.disconnect()

def data2list(filename):
    f = open(filename, "r")
    temp = []
    for row in f:
        temp.append(row.replace("\n",""))
    return temp
       
csecret=raw_input("Please enter consumer secret: ")
asecret=raw_input("Please enter access secret: ")

ckey="YwZ1bA48rbhgi3IN36bmT5z0m"
atoken="178696682-7B92NpYED29UWzy8j3M1Mi6d6i43CQwK4bjOthAX"
stream=MyStreamer(ckey,csecret,atoken,asecret)

keywords = data2list("/home/masdarcis/Projects/remote_projects/oilprice_analysis/keywords.data")
stream.statuses.filter(track=",".join(keywords), locations="52.087480,22.667618,55.262529,23.868627,52.087480,23.868627,56.026079,24.739715,54.867021,24.744704,56.432573,26.039873")