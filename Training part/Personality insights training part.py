import csv
import array
import pandas
import pickle
import pprint
import os
import sys
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import GaussianNB
from sklearn import svm
csvFile=open('CSV_Data/newfrequency300.csv', 'rt')
csvReader=csv.reader(csvFile)

mydict={row[1]: int(row[0]) for row in csvReader}



y=[]
print('Training Model for Judging/Perception ... \n')
with open ('CSV_Data/PJFinaltest.csv', 'rt') as f:
	reader=csv.reader(f)
	corpus=[rows[0] for rows in reader]

print('Reading data from file PJFinaltest.csv')
with open ('CSV_Data/PJFinaltest.csv', 'rt') as f:
	csvReader1=csv.reader(f)
	for rows in csvReader1:
		y.append([int(rows[1])])
vectorizer=TfidfVectorizer(vocabulary=mydict,min_df=1)
x=vectorizer.fit_transform(corpus).toarray()
result=np.append(x,y,axis=1)
X=pandas.DataFrame(result)
model=GaussianNB()
train = X.sample(frac=0.8, random_state=1)
test=X.drop(train.index)
y_train=train[301]
y_test=test[301]
print('Size of training data ' + str(train.shape))
print('Size of testing data ' + str(test.shape))
xtrain=train.drop(301,axis=1)
xtest=test.drop(301,axis=1)
model.fit(xtrain,y_train)
pickle.dump(model, open('Pickle_Data/BNPJFinal1.sav', 'wb'))
del result

y=[]

print('Training Model for Introversion/Extraversion ... \n')
with open ('CSV_Data/IEFinaltest.csv', 'rt') as f:
	reader=csv.reader(f)
	corpus=[rows[0] for rows in reader]

print('Reading data from file IEFinaltest.csv')
with open ('CSV_Data/IEFinaltest.csv', 'rt') as f:
	csvReader1=csv.reader(f)
	for rows in csvReader1:
		y.append([int(rows[1])])
vectorizer=TfidfVectorizer(vocabulary=mydict,min_df=1)
x=vectorizer.fit_transform(corpus).toarray()
result=np.append(x,y,axis=1)
X=pandas.DataFrame(result)
model=GaussianNB()
train = X.sample(frac=0.8, random_state=1)
test=X.drop(train.index)
y_train=train[301]
y_test=test[301]
print('Size of training data ' + str(train.shape))
print('Size of testing data ' + str(test.shape))
xtrain=train.drop(301,axis=1)
xtest=test.drop(301,axis=1)
model.fit(xtrain,y_train)
pickle.dump(model, open('Pickle_Data/BNIEFinal1.sav', 'wb'))
del result


y=[]
print('Training Model for Thinking/Feeling ... \n')
with open ('CSV_Data/TFFinaltest.csv', 'rt') as f:
	reader=csv.reader(f)
	corpus=[rows[0] for rows in reader]


print('Reading data from file TFFinaltest.csv')
with open ('CSV_Data/TFFinaltest.csv', 'rt') as f:
	csvReader1=csv.reader(f)
	for rows in csvReader1:
		y.append([int(rows[1])])

vectorizer=TfidfVectorizer(vocabulary=mydict,min_df=1)
x=vectorizer.fit_transform(corpus).toarray()
result=np.append(x,y,axis=1)
X=pandas.DataFrame(result)
model=GaussianNB()
train = X.sample(frac=0.8, random_state=1)
test=X.drop(train.index)
y_train=train[301]
y_test=test[301]
print('Size of training data ' + str(train.shape))
print('Size of testing data ' + str(test.shape))
xtrain=train.drop(301,axis=1)
xtest=test.drop(301,axis=1)
model.fit(xtrain,y_train)
pickle.dump(model, open('Pickle_Data/BNTFFinal1.sav', 'wb'))
del result


y=[]
print('Training Model for Sensing/Intuition ... \n')
with open ('CSV_Data/SNFinaltest.csv', 'rt') as f:
	reader=csv.reader(f)
	corpus=[rows[0] for rows in reader]
print('Reading data from file SNFinaltest.csv')
with open ('CSV_Data/SNFinaltest.csv', 'rt') as f:
	csvReader1=csv.reader(f)
	for rows in csvReader1:
		y.append([int(rows[1])])
vectorizer=TfidfVectorizer(vocabulary=mydict,min_df=1)
x=vectorizer.fit_transform(corpus).toarray()
result=np.append(x,y,axis=1)
X=pandas.DataFrame(result)
model=GaussianNB()
train = X.sample(frac=0.8, random_state=1)
test=X.drop(train.index)
y_train=train[301]
y_test=test[301]
print('Size of training data ' + str(train.shape))
print('Size of testing data ' + str(test.shape))
xtrain=train.drop(301,axis=1)
xtest=test.drop(301,axis=1)
model.fit(xtrain,y_train)
pickle.dump(model, open('Pickle_Data/BNSNFinal1.sav', 'wb'))


#print('\nSaving all the 4 models trained into a pickle file. ')