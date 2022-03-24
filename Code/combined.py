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


#ALL FUNCTIONS PRESENT IN THIS PYTHON FILE

#______________________________________________________________#

def getList(foldername):
    """ Return all the .txt files present in the data folder.
        Provides the dataframe to work on.
    """
    import glob
    dataset = [f for f in glob.glob(foldername+"/*.txt")] 
    return (dataset)

#______________________________________________________________#

def inverted_index(dataset):
    """ 
    Preprocesses the data and stemms the words.
    Creates inverted indexing of all the words in the corpus.
    Maps the words them to a set of documents in which they are present.
    Creates inverted indexing for all permuterms of a given key.
    """
    
    import nltk
    from nltk.tokenize import sent_tokenize , word_tokenize
    nltk.download('punkt')
    from collections import defaultdict    
    from nltk.stem import PorterStemmer
    from nltk.corpus import stopwords
    import re

    #creating a data structure for inverted indexing with key as stemmed words and values as set of documents
    inverted_index = defaultdict(set)
    
    #importing stopwords from nltk and making it into a set
    stwords = set(stopwords.words('english'))
    
    #importing the porterStemmer
    ps = PorterStemmer()

    s=dataset
    
    def remove_special_characters(text):
        import re
        regex = re.compile('[^a-zA-Z0-9\s]')
        text_returned = re.sub(regex,'',text)
        return text_returned
    
    for file in s:
        
        print(file)
        
        fname = file
        file = open(file , "r")
        text = file.read()
        
        #id=num
        #num+=1
        
        text=remove_special_characters(text)
        
        for sent in sent_tokenize(text):
            for word in word_tokenize(sent):
                word_lower = word.lower()
                if word_lower not in stwords:
                    #stemms the words
                    word_stem = ps.stem(word_lower)
                    
                    #doing indexing for all the permuterms possible
                    n=len(word_stem)
                    word_stem = word_stem + '$' 

                    while(n>=0):
                        word_stem=rotate(word_stem,1)
                        inverted_index[word_stem].add(fname)
                        n-=1
    return inverted_index

#______________________________________________________________#

def getClosest(word):
    '''
    Finds the closest word in the corpus related to the incorrect word passed by the User.
    '''
    dictionary = {}
    for w in inverted_index.keys():
        dist=editDist(word,w)
        dictionary[w]=dist
        if dist == 1:
            return w
    v=(sorted(dictionary.items(), key=lambda item: item[1]))
    return v[0][0]

#______________________________________________________________#

def editDist(word1, word2):
    '''
    Finds the distance between two similar words.
    '''
    m=len(word1)
    n=len(word2)
    
    dp = [[0 for x in range(n + 1)] for x in range(m + 1)]
 
    for i in range(m + 1):
        for j in range(n + 1):
            if i == 0:
                dp[i][j] = j    # Minimum possible operations for this case = j

            elif j == 0:
                dp[i][j] = i    # Minimum possible operations for this case = i
 
            elif word1[i-1] == word2[j-1]:
                dp[i][j] = dp[i-1][j-1]
 
            else:
                dp[i][j] = 1 + min(dp[i][j-1],        # Count Insert
                                   dp[i-1][j],        # Count Remove
                                   dp[i-1][j-1])      # Count Replace and find minimum
 
    return dp[m][n]
        
#______________________________________________________________#
        
def rotate(strg, n):
    '''
    Rotates a string n times to the left
    Performs a leftrotate operation on the string 
    '''
    return strg[n:] + strg[:n]

#______________________________________________________________#

def readFile(filename):
    '''
    Reads the file
    '''
    f=open(filename,"r")
    print(f.read())
    f.close()
    
#______________________________________________________________#

def count_files(foldername):
    '''
    Counts the number of files in a folder
    '''
    dataset= getList(foldername)
    count=0
    for file in dataset:
        count+=1
    return count

#______________________________________________________________#


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
while(True):

    print()
    print("Search Using AND,OR & NOT alongwith keywords.")
    print()
    print("Enter exit() in query to exit the program")
    print()
    print("Wildcard entries added.")
    print()

    query = input('Enter your query:')
    print("Wait while we're processing...")
    
    if query == "exit()":
        break
    
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
                #removing the star and checking for substr
                if '*' in word:
                    part=word[:-1]
                    partset=set()
                    for key in ii.keys():
                        if key.startswith(part):
                            keyset = set()
                            keyset=set(ii[key])
                            partset.update(keyset)

                    negated_set=(set(dataset).difference(set(partset))) #typecasting to set
                    q.append(negated_set)

                elif word in ii.keys():
                    set_a=ii[word]
                    negated_set=(set(dataset).difference(set(set_a))) #typecasting to set
                    q.append(negated_set)

                else:
                    cword=getClosest(word)
                    set_a=ii[cword]
                    negated_set=(set(dataset).difference(set(set_a)))
                    q.append(negated_set)
                continue

            if '*' in word:
                part=word[:-1]
                partset=set()
                for key in ii.keys():
                    if key.startswith(part):
                        keyset = set()
                        keyset=set(ii[key])
                        partset.update(keyset)
                q.append(partset)

            elif word in ii.keys():
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
