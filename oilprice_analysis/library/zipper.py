import pickle

#store the object
myObject = {'a':'blah','b':range(10)}
f = open('testPickleFile.pkl','w')
pickle.dump(myObject,f)
f.close()

#restore the object
f = open('testPickleFile.pkl','r')
myNewObject = pickle.load(f)
f.close()

print myObject
print myNewObject

Second, using gzip to create a compressed file:

import pickle
import gzip

#store the object
myObject = {'a':'blah','b':range(10)}
f = gzip.open('testPickleFile.pklz','wb')
pickle.dump(myObject,f)
f.close()

#restore the object
f = gzip.open('testPickleFile.pklz','rb')
myNewObject = pickle.load(f)
f.close()

print myObject
print myNewObject