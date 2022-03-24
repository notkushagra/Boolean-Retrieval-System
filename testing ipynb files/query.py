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



query = input('Enter your query:')
query= remove_special_characters(query)
query = query.lower()
query = word_tokenize(query)

connecting_words = []
# cnt = 1
different_words = []


ps=PorterStemmer()



def getClosest(word):
    dictionary = {}
    for w in ii.keys():
        dist=editDist(word,w)
        dictionary[w]=dist
        if dist == 1:
            return w
    v=(sorted(dictionary.items(), key=lambda item: item[1]))
    return v[0][0]

# Initializing a queue
q = deque()

for word in query:
    word=ps.stem(word)
    if word.lower() != "and" and word.lower() != "or" and word.lower() != "not":
        different_words.append(word.lower()+'$')
    else:
        connecting_words.append(word.lower())

print(connecting_words)
print(different_words)


allfiles=getList("testcase")

for word in different_words:
    if word in ii.keys():
        q.append(ii[word])
    else:
        cword=getClosest(word)
        q.append(ii[cword])

for connector in connecting_words:
    if connector == 'not':
        set_a= q.pop()
        q.appendleft(set(dataset).difference(set(set_a)))
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
print(outputset)
print(len(outputset))
