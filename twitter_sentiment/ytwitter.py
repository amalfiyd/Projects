from selenium import webdriver
from sys import stdout
import time,urllib,copy,re,numpy,pickle,csv,pdb,pydot,itertools,logging
 
# Regexs
namereg=re.compile("(.*?)@",re.DOTALL)
tweetidreg=re.compile("/status/(\d+)")
winreg=re.compile("window=(.+?)&")
wordreg=re.compile("\S+")
hashtagreg=re.compile("#[^\s?,.:]+",re.IGNORECASE)
 
# Some constants
march8=1394236856 # this is the timestamp for 12am march the 8th
dayseconds=86400
 
# Loading utility data
packagepath=re.compile('(.+?)[^/]+\.py').findall(__file__)[0]+'data/' # Determining pathname
if packagepath=="ydata/":
    packagepath="data/"
 
# Location (city, country name) data
countrydict=dict([(tmp[0],tmp[1]) for tmp in csv.reader(open(packagepath+"countryabbreviations_v2.csv"))])
citycsv=csv.reader(open(packagepath+'worldcitiespop.txt'))
# Creating city,country tuples for all cities with population data (ie bigger cities) and also changing to lower case and removing spaces
citycsv.next()
citiesdict=dict([(tmp[1].lower().replace(' ',''),countrydict[tmp[0]].lower()) for tmp in citycsv if tmp[4] != ''])
 
# Adding in the names of the states and other manually added locations
manualdict=dict([(tmp[0].lower().replace(' ',''),tmp[1].lower()) for tmp in csv.reader(open(packagepath+'manuallocationlist.csv'))])
citiesdict.update(manualdict);
 
citiesset=set(citiesdict.keys())
countryreg=re.compile("|".join(set(countrydict.values())),re.IGNORECASE)
citiespiecesreg=re.compile('[^,-/+\n]+')

#######################
# Utility functions
#######################

def DayToTime(inday):
    '''
    Takes day in # of days from 12am March 8
    and converts that to timestamp in miliseconds
    (Note: not seconds!)
    '''
    return 1000*(march8+inday*dayseconds)

def NormalizeTweets(tweetList=[]):
    
    if tweetList==[]:
        tweetList=RemoveDuplicates(MergePickleFiles())
        
    result=[]
    for tweet in tweetList:
        tmpTweet=copy.deepcopy(tweet)
        tmpTweet['text']=tmpTweet['text'].lower()
        tmpTweet['username']=tmpTweet['username'].lower()
        tmpTweet['name']=tmpTweet['name'].lower()
        tmpTweet['location']=tmpTweet['location'].lower()
        tmpTweet['map_location']=tmpTweet['map_location'].lower()
        result.append(tmpTweet)

    return result


def GroupTweetsByAuthor(tweetList=[],copyWholeStructure=False):
    if tweetList==[]:
        tweetList=NormalizeTweets()
    authorTweetDict={}
    for tweet in tweetList:
        try:
            authorTweetDict[tweet['username']]['text']+=" "+tweet['text']
        except KeyError:
            if copyWholeStructure:
                authorTweetDict[tweet['username']]=tweet
            else:
                tmp={}
                tmp['text']=tweet['text']
                tmp['username']=tweet['username']
                authorTweetDict[tweet['username']]=tmp
    return authorTweetDict.values()
    

def GenTopographic(distMat,nodeList,fileName="topohashtag"):
    '''
    Generate a topographic map from a list of hashtags
    And a distance matrix separating them
    '''
    
    # Encoding hashtag names properly
    nodeList=[tmp.encode('ASCII','ignore') for tmp in nodeList]
    
    # Creating pydot object
    graph=pydot.Dot(graph_type="graph");

    # Creating and adding nodes
    nodeDict={}
    for count in range(len(nodeList)):
        tmpNode=pydot.Node(nodeList[count])
        nodeDict[count]=tmpNode;
        graph.add_node(tmpNode);

    # Creating and adding edges
    for count1 in range(len(nodeList)):
        for count2 in range(count1+1,len(nodeList)):
            if distMat[count1,count2]>0:
                tmpEdge=pydot.Edge(nodeDict[count1],nodeDict[count2],len=str(distMat[count1,count2]))
                graph.add_edge(tmpEdge);
    
    graph.write_dot(fileName+".dot",prog="neato");

    
    


def GetSimMat(hashTags=[],numTags=100,tweets=[],tokenizer=hashtagreg,returnMatrix=True):
    '''
    Returns a matrix of similarities between hashtags for the corpus in variable "tweets"

    Parameters
    ==========
    tweets - the tweets (or any other corpus of texts) with which to calculate the 
     co-occurence statistics. Can be provided in two ways: either as a list of 
     strings (ie tweets) or as a list of tweet structures obtained using
     MergePickleFiles (each of which is obtained using GetTweetInfo etc)
    hashTags - if provided, then these are used, otherwise 
    the numTags top tags will be extracted and used. Returned 
     value is a tuple (simMat,hashTags)
    tokenizer - the regular expression used to extract tokens. By default this will 
     detect hashtags only (which is more efficient) but can use the "wordreg" for e.g.
    returnMatrix - True to return the result as a similarity matrix, and False to return it
     as a list of edges
    '''

    if tweets==[]:
        tweets=[tmp['text'] for tmp in NormalizeTweets()]
    else:
        try:
            tweets=[tmp['text'].lower() for tmp in tweets]
        except TypeError:
            if type(tweets[0])==type('') or type(tweets[0])==type(u''):
                tweets=[tmp.lower() for tmp in tweets]
            else:
                raise TypeError('Argument tweets is not of the correct type')

    if hashTags==[]:
        hashTags=[tmp[0] for tmp in TopN(tokenizer.findall(" ".join(tweets)),numTags)]
    else:
        numTags=len(hashTags)

    hashTagSet=set(hashTags)
    nodeIndex=dict(zip(hashTags,range(numTags)))
    simMat=numpy.zeros((numTags,numTags))
    # Laplace correction style fix
    freqVec=numpy.ones(numTags)*0.1;
    
    for text in tweets:
        tags=[tmp for tmp in tokenizer.findall(text) if tmp in hashTagSet]
        for tag in tags:
            freqVec[nodeIndex[tag]]+=1;
        for count1 in range(len(tags)):
            for count2 in range(count1+1,len(tags)):
                ind1=nodeIndex[tags[count1]]
                ind2=nodeIndex[tags[count2]]
                if ind1!=ind2:
                    simMat[ind1,ind2]+=1.0
                    simMat[ind2,ind1]+=1.0
                    
    # pdb.set_trace()

    # Normalizing
    for count1 in range(numTags):
        for count2 in range(count1+1,numTags):
            normalizer=min([freqVec[count1],freqVec[count2]])
            simMat[count1,count2]=simMat[count1,count2]/normalizer
            simMat[count2,count1]=simMat[count2,count1]/normalizer           
            
            
    if returnMatrix:
        return (simMat,hashTags)
    else:
        # Convert to Edge List
        edgeList=[]
        for count1 in range(numTags):
            for count2 in range(count1+1,numTags):
                if simMat[count1,count2]>0:
                    edgeList.append((hashTags[count1],hashTags[count2],simMat[count1,count2]))

        # Checking for missing nodes - i.e. nodes which simply do not co-occur with any other items
        # If found, add a link to all other nodes that is half the smallest similarity
        tmpHashTagSet=set(itertools.chain(*[[tmp[0],tmp[1]] for tmp in edgeList]))
        diffSet=hashTagSet.difference(tmpHashTagSet)
        if len(diffSet)>0:
            minSim=numpy.array([tmp[2] for tmp in edgeList]).min()
            for missingTag in hashTagSet.difference(tmpHashTagSet):
                for tag in tmpHashTagSet:
                    logging.warning("ytwitter.py/GetSimMat - missing node filled in: "+missingTag)
                    edgeList.append((missingTag,tag,minSim/2))
                    #pdb.set_trace()
        return edgeList



def TopN(itemList,N=-1,excludeList=['']):
    '''
    Provide a list of the top N most frequent items in a list of items
    sorted in decreasing frequency. Returns list of tuples of (items,frequency)
    by default N is the number of items in the list.
    excludeList is the list of items to be excluded from the counting,
    by default occurrences of '' are ignored
    '''
    freqdict={}
    excludeSet=set(excludeList);
    for item in (tmp for tmp in itemList if tmp not in excludeSet):
        try:
            freqdict[item]+=1
        except KeyError:
            freqdict[item]=1
    
    if N==-1:
        N=len(freqdict.keys())

    return sorted(freqdict.items(),lambda x,y:cmp(x[1],y[1]),reverse=True)[0:N]
    


def MergePickleFiles(datalist=[],filelist=['mh370.pkl','mh370_set2.pkl','mh370_topsy.pkl','mh370_topsy_set2.pkl','mh370_assorted.pkl','mh370_assorted_topsy.pkl','mh370_realtime.pkl']):
    '''Merge pickled tweet data files into a single list of tweets
    Default is to receive a list of filenames, but can also provide a list of
    tweet data structures such as the ones created using the data_collection scripts'''
    inputdata_list=filelist
    if datalist!=[]:
        inputdata_list=datalist
    
    merged=[]
    for indata in inputdata_list:
        
        try:
            mh=pickle.load(open(indata))
        except TypeError:
            mh=indata
        
        for key in mh.keys():
            merged=MergeTweets(mh[key],merged)
    
    return merged

def RemoveDuplicates(tweetlist,rejected=[]):
    '''
    Remove duplicate tweets based on tweetid
    the "rejected" parameter is to be used to store values of rejected tweets
    these will be entered directly into the variable (in-place) BE CAREFUL!
    '''
    accepted=[]
    idset=set([])
    for tweet in tweetlist:
        if tweet['tweetid'] not in idset:
            idset.update([tweet['tweetid']])
            accepted.append(tweet)
        else:
            rejected.append(tweet)
    return accepted


def ScrollBottom(browser):
    '''Scrolls to the bottom of the browser window'''
    browser.execute_script("window.scrollTo(0,Math.max(document.documentElement.scrollHeight," + "document.body.scrollHeight,document.documentElement.clientHeight));");

def GetTweetInfo(tweet):
    '''Takes a tweet structure extracted from the twitter search
    webpage (from the class="tweet" div), and converts it into
    a dict with the relevant fields'''
    result={}
    result["text"]=tweet.find_elements_by_class_name("tweet-text")[0].text
    result["username"]=tweet.get_attribute("data-screen-name")
    result["userid"]=tweet.get_attribute("data-user-id")
    result["name"]=tweet.get_attribute("data-name")
    result["tweetid"]=tweet.get_attribute("data-tweet-id")
    result["timestamp"]=tweet.find_element_by_class_name("tweet-timestamp").get_attribute("title")
    result["timestamp_ms"]=tweet.find_element_by_class_name("_timestamp").get_attribute("data-time-ms")
    try:
        result["location"]=tweet.find_element_by_class_name("tweet-geo-text").text
        result["map_location"]=tweet.find_element_by_class_name("tweet-geo-text").find_element_by_tag_name("a").get_attribute("href")
    except:
        result["location"]=""
        result["map_location"]=""

    return result

def GetTweetInfoTopsy(tweet):
    '''Takes a tweet structure extracted from topsy
    and converts it into a dict with the relevant fields'''
    result={}
    result["text"]=tweet.find_element_by_class_name("media-body").find_element_by_tag_name("div").text
    result["username"]=tweet.find_element_by_class_name("media-heading").find_element_by_tag_name("small").text[1:]
    result["userid"]=''
    result["name"]=namereg.findall(tweet.find_element_by_class_name("media-heading").find_element_by_tag_name("a").text)[0].rstrip()
    result["tweetid"]=tweetidreg.findall(tweet.find_element_by_class_name("muted").get_attribute("href"))[0]
    result["timestamp"]=''
    result["timestamp_ms"]=tweet.find_element_by_class_name("relative-date").get_attribute("data-timestamp")+"000"
    result["location"]=""
    result["map_location"]=""

    return result

def MergeTweets(tweets1,tweets2):
    '''
    Takes two sets of tweets (created by GetTweets)
    and merges into a set of unique tweets based on the tweetids
    '''
    ids1=set([tmp["tweetid"] for tmp in tweets1])
    result=copy.deepcopy(tweets1);
    result.extend([tmp for tmp in tweets2 if tmp["tweetid"] not in ids1])
    return result    

def Location2Country(location):
    '''
     Takes the location info
     from the user data (obtained using twitter API)
     and returns a best guess of the country
    '''

    # First look for direct mentions of country names
    try:
        return countryreg.findall(location)[0].lower()
    except IndexError:
        pass
    except AttributeError:
        pdb.set_trace()

    # Try to break location into comma (and similarly) separated pieces and search in cities
    pieces=[tmp.strip().lower().replace(' ','') for tmp in citiespiecesreg.findall(location)]
    for piece in pieces:
        if piece in citiesset:
            return citiesdict[piece].lower()

    # Try breaking into individual word (space separated)
    pieces=[tmp.lower() for tmp in wordreg.findall(location)]
    for piece in pieces:
        if piece in citiesset:
            return citiesdict[piece].lower()
            
    # Give up.
    return ''

LocationToCountry=Location2Country

######################################################################################
# Utility classes
######################################################################################

# Returns a value from a dict, but returns a "notfound" value if the key is not found
class RobustDict(dict):

    notFound=''

    def __init__(self,*args,**kwargs):
        dict.__init__(self,*args)
        if "notFound" in kwargs.keys():
            self.notFound=kwargs["notFound"]

    def __getitem__(self,inkey):
        try:
            return dict.__getitem__(self,inkey)
        except KeyError:
            return self.notFound

        
#####################################################################################################################
# Functions to retrieve data from twitter and/or topsy
#####################################################################################################################

def GetTweets(searchTerm,numRequested=20,numTries=5,pauseLength=0.8,realTime=False,browser=''):
    '''
    Gets the tweets. Will try to get at least numRequested tweets
    but may not be exactly this number
    Note: the pauseLength of 0.8 seems a good number, heuristically
    '''

    # Initializations
    ##################
    numResponses=0
    tries=iter(range(1,numTries+1))


    # Starting up webbrowser and loading pages
    ############################################
    closeBrowser=False;
    if browser=='':
        closeBrowser=True;
        browser = webdriver.Firefox()
    urlstr="https://twitter.com/search?q="+urllib.quote(searchTerm,"%")+"&src=typd"    
    if realTime:
        urlstr="https://twitter.com/search?f=realtime&q="+urllib.quote(searchTerm,"%")+"&src=typd" 
    browser.get(urlstr)

    #browser.get('http://search.twitter.com')
    #searchForm=browser.find_element_by_id("search-query")
    #searchForm.send_keys(searchTerm)
    #searchForm.submit()

    time.sleep(pauseLength)

    # Collecting tweets
    ###################
    numWaits=1;
    while numResponses<numRequested:
        time.sleep(pauseLength*numWaits)
        responses=browser.find_elements_by_class_name("tweet")
        if numResponses==len(responses):
            numWaits+=1;
            n=tries.next()
            stdout.write("Try #"+str(n)+": nothing new retrieved\n");
            if n==numTries:
                print "Sorry only able to retrieve "+str(numResponses)+" tweets."
                break
        else:
            # Scroll down and get next set of tweets
            numWaits=1;
            print "Retrieved "+str(len(responses))+" tweets so far..."
            ScrollBottom(browser)
            tries=iter(range(1,numTries+1))
            numResponses=len(responses);

    result=[GetTweetInfo(tmp) for tmp in responses]
    if closeBrowser:
        browser.close()
    return result

def GetTweetsTopsy(searchTerm,numRequested=20,numTries=5,pauseLength=0.8,realTime=False,mintime='',maxtime='',browser='',startOffset=0):
    '''
    Gets tweets from topsy.
    Note that the numRequested means that the function will try to return at least
    that number of unique tweets. It may (will probably) return more, and there may be
    some duplicates. Can use "RemoveDuplicates" to sort this out later.
    '''

    # Starting up webbrowser and loading pages
    ############################################
    closeBrowser=False;
    if browser=='':
        closeBrowser=True;
        browser = webdriver.Firefox()
    
    # Collecting tweets
    ###################
    timestr=''
    if mintime != '':
        timestr="&mintime="+str(mintime)
    if maxtime != '':
        timestr=timestr+"&maxtime="+str(maxtime)

    browser.get("http://topsy.com/s?q="+urllib.quote(searchTerm,"%")+"&type=tweet"+timestr)
    try:
        winlabel="&window="+winreg.findall(browser.find_element_by_class_name("pagination").find_element_by_tag_name("a").get_attribute("href"))[0]
    except:
        winlabel=''

    result=[]
    numResponses=0
    offsetiter=iter(xrange(startOffset,1000000,10));
    while numResponses<numRequested:
        
        offset=offsetiter.next()
        if offset>0:
            urlstr="http://topsy.com/s?q="+urllib.quote(searchTerm,"%")
            urlstr=urlstr+winlabel+"&type=tweet&offset="+str(offset)+timestr      
            browser.get(urlstr)
        
        tmpRes=browser.find_elements_by_class_name("result-tweet")
        if len(tmpRes)==0:
            numResponses=len(set([tmp["tweetid"] for tmp in result]))
            print "Sorry only able to retrieve "+str(numResponses)+" tweets."
            break
        result.extend([GetTweetInfoTopsy(tmp) for tmp in tmpRes])

        numResponses=len(set([tmp["tweetid"] for tmp in result]))
        print "Retrieved "+str(numResponses)+" tweets so far..."

    if closeBrowser:
        browser.close()

    return result


