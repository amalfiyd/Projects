import csv
import nltk
import string
import collections
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD

# Load stopwords from nltk stopwords corpus
# stopset = stopwords.words("english")
stopset = []
porter_stemmer = PorterStemmer()
word_lemmatizer = WordNetLemmatizer()

abstracts = []

# Add additional stopwords
with open('additional_stopwords.txt','rb') as myfile:
	for line in myfile:
		if line.rstrip not in stopset:
			stopset.append(line.rstrip())

# Vectorizing
with open('ai_cis606_project3.csv','rb') as csvfile:
	dataset = csv.reader(csvfile, delimiter=',', quotechar='"')
	csvfile.readline()
	i = 1
	for row in dataset:
		sentence = row[3].lower()
		sentence = filter(lambda x : x in string.printable, sentence)
		tokens = nltk.word_tokenize(sentence)
		tokens = filter(str.isalpha, tokens)

		stopworded = list(t for t in tokens if t not in stopset and t not in string.punctuation)
		preprocessed = map(lambda x : word_lemmatizer.lemmatize(x), stopworded)
		# preprocessed = map(lambda x : porter_stemmer.stem(x), preprocessed)

		sentence = " ".join(t for t in preprocessed)

		abstracts.append(sentence)
		print i, " out of : ", 21959 
		# if i == 5000:
		# 	break
		i = i + 1

print "Vectorizing..."
vectorizer = TfidfVectorizer(use_idf=True)
X = vectorizer.fit_transform(abstracts)
print X.shape

# SVD
lsa = TruncatedSVD(n_components=100, n_iter=100, algorithm='arpack')
lsa.fit(X)

terms = vectorizer.get_feature_names()
for i, comp in enumerate(lsa.components_):
	termsInComp = zip(terms, comp)
	sortedTerms = sorted(termsInComp, key=lambda x: x[1], reverse=True) [:10]
	print "Concept : ",i
	for term in sortedTerms:
		print term[0]
	print " " 

print "Finish!"