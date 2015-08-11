from twython import Twython,TwythonStreamer
import pickle,time,re
import bz2, gzip

def save_zipped_pickle(obj, filename, protocol=-1):
    with gzip.open(filename, 'wb') as f:
        pickle.dump(obj, f, protocol)

def load_zipped_pickle(filename):
    with gzip.open(filename, 'rb') as f:
        loaded_object = pickle.load(f)
        return loaded_object

consumer_secret = "Bnc57NoMFduN61XGGrHXAWdC8VYfY1WcKWIVpVgX7OL1W9W7Q1"
access_token_secret = "nGsurl7tvNoOTtBLr2AItLZlCw9i9Ev5SDuOPqCvOJdYd"
outdir = "oilprice/"
trackfile = open("oilprice.wrd","r")

# locationsfile = open(libdir+"/locations/u_states.pos","r")

result=[]
class MyStreamer(TwythonStreamer):

    def on_success(self, data):
        global result
        if 'text' in data:
            print "Result entry #"+str(len(result)+1)+data['text'].encode('utf-8')
            result.append(data)
            if len(result)==1000:
                filetag=re.sub("\s","_",time.ctime())
                filename = outdir+"twitterstream_"+filetag+".pkl"
                save_zipped_pickle(result, filename)
                result=[]

    def on_error(self, status_code, data):
        print status_code

        # Want to stop trying to get data because of the error?
        # Uncomment the next line!
        self.disconnect()

        mytrack=[]
        for row in trackfile:
            split_string = row.split(" ")
            if(len(split_string) > 1):
                temp = row.replace("\n","").replace("\r","")
                mytrack.append(temp)
        
        stream.statuses.filter(track=",".join(mytrack), languange='en')

# csecret=raw_input("Please enter consumer secret: ")
# asecret=raw_input("Please enter access secret: ")

csecret = consumer_secret
asecret = access_token_secret

ckey="YwZ1bA48rbhgi3IN36bmT5z0m"
atoken="178696682-7B92NpYED29UWzy8j3M1Mi6d6i43CQwK4bjOthAX"
stream=MyStreamer(ckey,csecret,atoken,asecret)

# mylocations=[]
# for row in locationsfile:
#     temp = row.replace("\n","").replace("\r","")
#     mylocations.append(temp)

mytrack=[]
for row in trackfile:
    split_string = row.split(" ")
    if(len(split_string) > 1):
        temp = row.replace("\n","").replace("\r","")
        mytrack.append(temp)

# stream.statuses.filter(track=",".join(mytrack), locations=",".join(mylocations), languange='en')
stream.statuses.filter(track=",".join(mytrack), languange='en')
