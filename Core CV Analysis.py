#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#PERSONALITY PREDICTION FOR A JOB THROUGH MACHINE LEARNING (NATURAL LANGUAGE PROCESSING)


# In[7]:


import PyPDF2

import os,os.path

from sklearn.feature_extraction.text import CountVectorizer

from sklearn.metrics.pairwise import cosine_similarity

import re

import string

from nltk.corpus import stopwords

from nltk.tokenize import word_tokenize 


# In[8]:


DIR = 'C:/Users/Administrator/Desktop/Resumes'

len_dir=len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])


# In[9]:


def clean_text(text):
    
    text=re.sub('<.*?>', ' ', text)  
    
    text = text.translate(str.maketrans(' ',' ',string.punctuation))
    
    text = re.sub('[^a-zA-Z]',' ',text)  
    
    text = re.sub("\n"," ",text)
    
    text = text.lower()
    
    text=' '.join(text.split())
    return text


# In[11]:


res_output = [] 
des_output = [] 
ls = []




for i in range(0,len_dir):
    mypath=r'C:\Users\Administrator\Desktop\Resumes'
    
    onlyfiles = [os.path.join(mypath, f) for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath, f))]

    
    
    
    resume = open(onlyfiles[i],'rb')
    
    pdfReader = PyPDF2.PdfFileReader(resume)

    pageObject = pdfReader.getPage(0)
    
    resume=pageObject.extractText()
    
    resume=clean_text(resume)
    
    
    
    
    
    stop_words = set(stopwords.words('english'))
    
    word_tokens = word_tokenize(resume) 
    
    for w in word_tokens: 
        
        if w not in stop_words:  
            
            res_output.append(w)
            
    resume= ' '.join([str(elem) for elem in res_output])
    
    res_output.clear()

    
    
    
    
    
    job_description=open('C:/Users/Administrator/Desktop/ML project/Python_developer.pdf','rb')
    
    pdfReader = PyPDF2.PdfFileReader(job_description)

    
    
    pageObject = pdfReader.getPage(0)
    
    job_description=pageObject.extractText()
    
    job_description=clean_text(job_description)
    
    
    
    
    stop_words = set(stopwords.words('english'))
    
    word_tokens = word_tokenize(job_description) 
    
    for y in word_tokens: 
        
        if y not in stop_words:  
            
            des_output.append(y)
            
    job_description= ' '.join([str(eleme) for eleme in des_output])
    
    des_output.clear()
    
    
    
    

    text = [resume, job_description]
    
    cv = CountVectorizer(lowercase=True, stop_words = 'english')
    
    count_matrix = cv.fit_transform(text)
    
    matchPercentage = cosine_similarity(count_matrix)[0][1] * 100
    
    matchPercentage = round(matchPercentage)

    
    
    path,file_name = os.path.split(onlyfiles[i])
    
    ls.append(( matchPercentage,file_name))
    
ls = sorted(ls, reverse = True)



print("\033[1m ORDER OF PERSON MATCHES FOR THE JOB\033[0m")


for m in ls:
    
    print(m[1]," this person matches about ",m[0],"% for the job")
    



# In[ ]:


#Thankyou/AREEBMAHFOOZTK

