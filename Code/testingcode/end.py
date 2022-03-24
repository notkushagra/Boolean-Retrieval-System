#!/usr/bin/env python
# coding: utf-8

# In[1]:


import nltk
from nltk.tokenize import sent_tokenize , word_tokenize
nltk.download('punkt')

from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

import glob
import re
import os
import numpy as np
import sys

from collections import defaultdict
from collections import deque
from functions import *


# In[2]:


foldername='data'
dataset=getList(foldername)
# print(dataset)


# In[3]:


ii=inverted_index(dataset)

freq_dict= {key: len(value) for key, value in ii.items()}
#To get the frequency of each key and its permuterm

# print(ii.keys())
# print(freq_dict)


# In[4]:


#Taking in query from the user
print()
print("Search Using AND,OR & NOT alongwith keywords.")
print()
print("Wildcard entries added.")
print()

query = input('Enter your query:')
print("Wait while we're processing...")

query = query.lower()
query_tokens=query.split()

connecting_words = []
different_words = []

ps=PorterStemmer()

def getClosest(word):
    '''
    Function returns the closest word in the dictionary.
    '''
    dictionary = {}
    for w in ii.keys():
        dist=editDist(word,w)
        dictionary[w]=dist
        if dist == 1:
            return w
    v=(sorted(dictionary.items(), key=lambda item: item[1]))
    return v[0][0]            #returns the key of the first key-value pair

# Initializing a queue 
q = deque()

for word in query_tokens:
    word=ps.stem(word)
    
    if word.lower() != "and" and word.lower() != "or" and word.lower() != "not":
        word=word+'$'
        
        if '*' in word:
            while(word[-1]!='*'):
                word=rotate(word,1) #to get * at the end of the search word
        
        different_words.append(word.lower())
        
        #check if we need to apply not operation on this word
        if len(connecting_words)>0 and connecting_words[-1]=="not":
            if word in ii.keys():
                set_a=ii[word]
                negated_set=(set(dataset).difference(set(set_a))) #typecasting to set
                q.append(negated_set)
            else:
                cword=getClosest(word)
                set_a=ii[cword]
                negated_set=(set(dataset).difference(set(set_a)))
                q.append(negated_set)
            continue
        
        
        if word in ii.keys():
            q.append(ii[word])
            
        else:
            cword=getClosest(word)
            q.append(ii[cword])
            
    else:
        connecting_words.append(word.lower())

# print(connecting_words)
# print(different_words)

# allfiles=getList("testcase")

for connector in connecting_words:
    if connector == 'not':
        continue
#         set_a= q.pop()
#         q.appendleft(set(dataset).difference(set(set_a)))

    elif connector == 'and':
        set_a = q.pop()
        set_b = q.pop()
        intersected=set(set_a).intersection(set(set_b))
        q.appendleft(intersected)
        
    elif connector == 'or':
        set_a = q.pop()
        set_b = q.pop()
        unioned=set(set_a).union(set(set_b))
        q.appendleft(unioned)

outputset=q.pop()
print("Matched Documents : " + str(len(outputset)))
print()
print(*outputset,sep='\n')
print()



# In[ ]:




