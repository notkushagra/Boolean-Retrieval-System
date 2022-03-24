import nltk
from nltk.tokenize import sent_tokenize , word_tokenize
nltk.download('punkt')

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer, PorterStemmer

import glob
import re
import os
import numpy as np
import sys

from collections import defaultdict
from functions import *



#Taking input
foldername = "testdata"; #foldername of directory containing all text files
dataset = getList(foldername)

#Getting all the stopwords of English Language
stopwords_list=(stopwords.words('english'))

ii=inverted_index(dataset)

# ii=allpermutation(ii)
