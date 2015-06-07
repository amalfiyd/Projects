import csv
import nltk
import string
import collections
import numpy as np
import time
import math

from random import randint
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer

#------------------------------------------
# ------------ HELPER FUNCTION ------------ 
def randomNormalizedProbs(size):
	output = []
	total = 0
	for i in range(0, size):
		output.append(randint(1,size))
		total = total + output[i]

	for i in range(0, size):
		output[i] = output[i] / float(total)

	return output

def avoidZero(input):
	if input == 0.0:
		return smallFloat
	else :
		return input
#----------------------------------------
# ------------ PREPROCESSING ------------ 
# Load stopwords from nltk stopwords corpus
# stopset = stopwords.words("english")
# print "Preprocessing..."
# stopset = []
# porter_stemmer = PorterStemmer()
# word_lemmatizer = WordNetLemmatizer()

# abstracts = []
# words = []

# # Add additional stopwords
# with open('additional_stopwords.txt','rb') as myfile:
# 	for line in myfile:
# 		if line.rstrip not in stopset:
# 			stopset.append(line.rstrip())

# # Feature extract
# with open('ai_cis606_project3.csv','rb') as csvfile:
# 	dataset = csv.reader(csvfile, delimiter=',', quotechar='"')
# 	csvfile.readline()
# 	i = 1
# 	for row in dataset:
# 		sentence = row[3].lower()
# 		sentence = filter(lambda x : x in string.printable, sentence)
# 		tokens = nltk.word_tokenize(sentence)
# 		tokens = filter(str.isalpha, tokens)

# 		stopworded = list(t for t in tokens if t not in stopset and t not in string.punctuation)
# 		preprocessed = map(lambda x : word_lemmatizer.lemmatize(x), stopworded)
# 		# preprocessed = map(lambda x : porter_stemmer.stem(x), preprocessed)
		
# 		words.extend(t for t in preprocessed if t not in words)
# 		sentence = " ".join(t for t in preprocessed)

# 		abstracts.append(sentence)
# 		print i, " out of : ", 21959 
# 		if i == 200:
# 			break
# 		i = i + 1

# # Sort the words
# words.sort()
# # Remove 1 character words
# words = list(t for t in words if len(t) > 1)

# # Vectorizing
# print "Vectorizing features..."
# # vectorizer = TfidfVectorizer(use_idf=False)
# vectorizer = CountVectorizer(vocabulary=words)
# docTermMatrix = vectorizer.fit_transform(abstracts)
# print docTermMatrix.shape

tic = time.clock()
# dataset = np.genfromtxt("preprocessed_pca.csv", delimiter=',')
dataset = docTermMatrixPCA
toc = time.clock()

print "Loaded in : ", toc - tic, " seconds"

#--------------------------------------------------------
# ------------ VARIABLES DEFINITION FOR pLSA ------------ 
print "Initializing variables..."
tic = time.clock()
topicNum = 2
docSize = dataset.shape[0]
vocabularySize = dataset.shape[1]
maxIter = 1
smallFloat = 0.00000000000000000001

# Parameters of Theta
# p(d|z)
pd_z = np.zeros((topicNum,docSize))
# p(w|z)
pw_z = np.zeros((topicNum,vocabularySize))
# p(z), prior of latent classes
start_prior = 1 / float(topicNum)
pz = np.zeros(topicNum)

# p(z|d,w)
pz_dw = np.zeros((topicNum, docSize, vocabularySize))
toc = time.clock()

print "Initializing done in : ", toc - tic
#----------------------------------------------------
# ------------ E STEP AND M STEP PROGRAM ------------
def e_step():
	# E-step, find "posterior" of instances using given parameters Theta, i.e. p(z), p(w|z), p(d|z)
	# i.e. filling the p(z|d,w) matrix
	for j in range(0, docSize):
		for k in range(0, vocabularySize):
			norm = 0.0
			for i in range(0, topicNum):
				val = pz[i] * pd_z[i,j] * pw_z[i,k]
				pz_dw[i, j, k] = val
				norm = norm + val 
			for i in range(0, topicNum):
				pz_dw[i, j, k] = pz_dw[i, j, k] / float(norm)
def m_step():
	# M-step, updating parameters Theta, i.e. p(z), p(w|z), p(d|z), given the observation
	# p(w|z)
	for i in range(0, topicNum):
		norm = 0.0
		for k in range(0, vocabularySize):
			_sum = 0.0
			for j in range(0, docSize):
				_sum = _sum + (dataset[j,k] * pz_dw[i,j,k])

			pw_z[i,k] = _sum
			norm = norm + _sum

		if norm == 0.0:
			norm = avoidZero(_norm)

		for k in range(0, vocabularySize):
			pw_z[i,k] = pw_z[i,k] / float(norm)

	# p(d|z)
	for i in range(0, topicNum):
		norm = 0.0
		for j in range(0, docSize):
			_sum = 0.0
			for k in range(0, vocabularySize):
				_sum = _sum + (dataset[j,k] * pz_dw[i,j,k])

			pd_z[i,j] = _sum
			norm = norm + _sum

		if norm == 0.0:
			norm = avoidZero(norm)

		for j in range(0, docSize):
			pd_z[i,j] = pd_z[i,j] / float(norm)

	# p(z)
	norm = 0.0
	for i in range(0, topicNum):
		_sum = 0.0
		for j in range(0, docSize):
			for k in range(0, vocabularySize):
				_sum = _sum + (dataset[j,k] * pz_dw[i,j,k])

		pz[i] = _sum
		norm = norm + _sum

	if norm == 0.0:
		norm = avoidZero(norm)

	for i in range(0, topicNum):
		pz[i] = pz[i] /  float(norm)


def logLikrlihood(p_z, pd_z, pw_z):
	L = 0.0
	for j in range(docSize):
		for k in range(vocabularySize):
			sum_ = 0.0
			for i in range(topicNum):
				sum_ = sum_ + p_z[i] * pd_z[i,j] * pw_z[i,k]

			L = L + math.log(sum_,2)

	return L

#-------------------------------------------------
# ------------ INITIALIZE FIRST STATE ------------ 
print "Initializing first state..."
tic = time.clock()
# p(z)
for i in range(0, topicNum):
	pz[i] = start_prior

# p(d|z)
for i in range(0, topicNum):
	temp = randomNormalizedProbs(docSize)
	for j in range(0, docSize):
		pd_z[i,j] = temp[j]

# p(w|z)
for i in range(0, topicNum):
	temp = randomNormalizedProbs(vocabularySize)
	for j in range(0, vocabularySize):
		pw_z[i,j] = temp[j]
toc = time.clock()

print "First parameters in : ", toc-tic

#-------------------------------------------
# ------------ RUN EM ALGORITHM ------------
print "Running EM optimization..."
t1 = 0
t2 = 0
for iteration in range(0, maxIter):
	if iteration == 0:
		t1 = time.clock()
	a = time.clock()
	e_step()
	b = time.clock()
	print "E-step in ", b - a
	a = time.clock()
	m_step()
	b = time.clock()
	print "M-step in ", b - a
	# a = time.clock()
	# L = logLikrlihood(pz, pd_z, pw_z)
	# b = time.clock()
	# print "logLikrlihood in ", b - a 
	# print "logLikrlihood : ", L, " at iteration ", iteration, " out of ", maxIter  

	print iteration, " out of ", maxIter
	if iteration == 0:
		t2 = time.clock()
		print "1 iteration requires : ", t2-t1 

print "Program done!"

# -----------------------------------------------
# -----------------------------------------------
# -----------------------------------------------
# -----------------------------------------------
# -----------------------------------------------

# # E-step, find "posterior" of instances using given parameters Theta, i.e. p(z), p(w|z), p(d|z)
# # i.e. filling the p(z|d,w) matrix
# for j in range(0, docSize):
# 	for k in range(0, vocabularySize):
# 		norm = 0.0
# 		for i in range(0, topicNum):
# 			val = pz[i] * pd_z[i,j] * pw_z[i,k]
# 			pz_dw[i, j, k] = val
# 			norm = norm + val 
# 		for i in range(0, topicNum):
# 			pz_dw[i, j, k] = pz_dw[i, j, k] / float(norm)

# # M-step, updating parameters Theta, i.e. p(z), p(w|z), p(d|z), given the observation
# # p(w|z)
# for i in range(0, topicNum):
# 	norm = 0.0
# 	for k in range(0, vocabularySize):
# 		_sum = 0.0
# 		for j in range(0, docSize):
# 			_sum = _sum + (docTermMatrix[j,k] * pz_dw[i,j,k])

# 		pw_z[i,k] = _sum
# 		norm = norm + _sum

# 	if norm == 0.0:
# 		norm = avoidZero(_norm)

# 	for k in range(0, vocabularySize):
# 		pw_z[i,k] = pw_z[i,k] / float(norm)

# # p(d|z)
# for i in range(0, topicNum):
# 	norm = 0.0
# 	for j in range(0, docSize):
# 		_sum = 0.0
# 		for k in range(0, vocabularySize):
# 			_sum = _sum + (docTermMatrix[j,k] * pz_dw[i,j,k])

# 		pd_z[i,j] = _sum
# 		norm = norm + _sum

# 	if norm == 0.0:
# 		norm = avoidZero(norm)

# 	for j in range(0, docSize):
# 		pd_z[i,j] = pd_z[i,j] / float(norm)

# # p(z)
# norm = 0.0
# for i in range(0, topicNum):
# 	_sum = 0.0
# 	for j in range(0, docSize):
# 		for k in range(0, vocabularySize):
# 			_sum = _sum + (docTermMatrix[j,k] * pz_dw[i,j,k])

# 	pz[i] = _sum
# 	norm = norm + _sum

# if norm == 0.0:
# 	norm = avoidZero(norm)

# for i in range(0, topicNum):
# 	pz[i] = pz[i] /  float(norm)