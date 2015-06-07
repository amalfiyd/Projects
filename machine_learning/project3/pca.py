import csv
import nltk
import string
import collections
import numpy as np
import time
import pylab as plot

from random import randint
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import PCA

def princomp2(A):
	print "1"
	M = (A.toarray()-np.mean(A.T.toarray(), axis=1)).T
	print "2"
	[latent, coeff] = np.linalg.eig(np.cov(M))
	print "3"
	score = np.dot(coeff.T, M)
	return coeff, score, latent

def princomp(A):
	print "1"
	M = (A-np.mean(A.T, axis=1)).T
	print "2"
	[latent, coeff] = np.linalg.eig(np.cov(M))
	print "3"
	score = np.dot(coeff.T, M)
	return coeff, score, latent

#----------------------------------------
# ------------ PREPROCESSING ------------ 
# Load stopwords from nltk stopwords corpus
# stopset = stopwords.words("english")
print "Preprocessing..."
stopset = []
porter_stemmer = PorterStemmer()
word_lemmatizer = WordNetLemmatizer()

abstracts = []
words = []

# Add additional stopwords
with open('additional_stopwords.txt','rb') as myfile:
	for line in myfile:
		if line.rstrip not in stopset:
			stopset.append(line.rstrip().lower())

# Feature extract
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
		preprocessed = map(lambda x : porter_stemmer.stem(x), preprocessed)
		
		words.extend(t for t in preprocessed if t not in words)
		sentence = " ".join(t for t in preprocessed)

		abstracts.append(sentence)
		print i, " out of : ", 21958 
		# if i == 100:
		# 	break
		i = i + 1

# Sort the words
words.sort()
# Remove 1 character words
words = list(t for t in words if len(t) > 1)

print "Vocabsize : ", len(words)

# Vectorizing
print "Vectorizing features..."
# vectorizer = TfidfVectorizer(use_idf=False)
vectorizer = CountVectorizer(vocabulary=words)
docTermMatrix = vectorizer.fit_transform(abstracts)
print docTermMatrix.shape

low_freq =  docTermMatrix.sum(axis=0)
docTermMatrixPCA = np.zeros((21958,1))
words_index = []

# Finding number of features with 90% variance & Remove low sum frequency features
# for i in range(len(words)):
# 	print i, " out of : ", len(words), " cleaning..."
# 	if low_freq[0,i] >= 10:
# 		docTermMatrixPCA = np.append(docTermMatrixPCA, docTermMatrix[:,i].toarray(),axis=1)
# 		words_index.append(i)

# docTermMatrixPCA = docTermMatrixPCA[:, 1:]
# print docTermMatrixPCA.shape

# print "Starting PCA..."
# tic = time.clock()
# coeff, score, latent = princomp(docTermMatrixPCA)
# perc = np.cumsum(latent) / sum(latent)
# toc = time.clock()

# print toc - tic

# plot.figure()
# axis = list(t+1 for t in range(len(words)))
# plot.stem(range(len(perc)), perc, 'bo')

# plot.show()

# with open("for_pca.csv", "w") as outcsv:
# 	writer = csv.writer(outcsv, delimiter=",")
# 	for i in range(0, 21959):
# 		print i, " out of : ", 21959
# 		writer.writerow(docTermMatrix.toarray()[i])

# print "Done!"

# pca = PCA()
# pca.fit(docTermMatrix.toarray())

# print "Count eigenvalues..."
# mean = [0 for x in range(len(words))]
# for i in range(0, len(words)):
# 	mean[i] = np.mean(docTermMatrix[:,i].toarray())

# # NEED TO BE UPDATED --> READ
# cov_mat = np.cov(docTermMatrix.T.toarray())
# eig_val_cov, eig_vec_cov = np.linalg.eig(cov_mat)