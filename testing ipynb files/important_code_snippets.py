#_____________________________________________________________________
all_words = []
dict_global = {}
file_folder = 'data/*'
idx = 1
files_with_index = {}
for file in glob.glob(file_folder):
    print(file)
    fname = file
    file = open(file , "r")
    text = file.read()
    
    text = remove_special_characters(text)
    text = re.sub(re.compile('\d'),'',text)
    sentences = sent_tokenize(text)
    words = word_tokenize(text)
    words = [word for word in words if len(words)>1]
    words = [word.lower() for word in words]
    words = [word for word in words if word not in stopwords_list]
    dict_global.update(finding_all_unique_words_and_freq(words))
    files_with_index[idx] = os.path.basename(fname)
    idx = idx + 1
    
unique_words = set(dict_global.keys())


#_____________________________________________________________________

from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
  
ps = PorterStemmer()

stemmed_global={}

for w in dict_global:
    stemw=ps.stem(w)
    if stemw in stemmed_global:
        stemmed_global[stemw]+= dict_global[w]
    else:
        stemmed_global[stemw]= dict_global[w]
unique_stems= set(stemmed_global.keys())
#_____________________________________________________________________

#counts the no of values in a particular key and create a new dictionary

length_dict = {key: len(value) for key, value in ii.items()}
length_key = length_dict['key']

#_______________________________________________________________

list(ii.items())[:3]

#_______________________________________________________________
