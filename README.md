<h1> Boolean Retrieval System </h1>

**Kushagra Singh 2019B1A70994H**

**Raj Srivastava 2019B1A71426H**

**Abhishek Jalan 2019B1A71547H**

**<h2>To run</h2>**
Go to the Code folder and compile and _**run the final.py**_ .

Make sure the appropriate libraries are download and can be accessed by the code.

In case of an error with function in the functions.py file 
1. Compile the functions.py file first

            or
  
2. Run the combined.py file

**<h2>Stopword Removal</h2>**

We imported **stopwords** from **nltk.corpus** library **.** All the english stopwords were stored in **stwords** variable. Now for all the keywords in the corpus, we check if these words are present in the the stwords. If they are present, such words are ignored, else they are added to the inverted index.

Example: &quot;Brutus and Caesar&quot;. Here the words &quot;Brutus&quot;, &quot;Caesar&quot; are added to the inverted index after further preprocessing while &quot;and&#39; is not since it is an English stopword.

**<h2>Stemming</h2>**

**PorterStemmer** is imported from the nltk.stem library. We pass the lowercase word in the stem() function of the PorterStemmer to get the stemmed word, which is used to create the inverted index.

Example: dreaming is stemmed to dream. Then further preprocessing takes place on the stemmed word.

**<h2>Building Index</h2>**

We created a dictionary named inverted\_index whose key represents all the keywords from the corpus and key&#39;s value is a set of documents in which that keyword is present.

i) **Removal of special characters**.removed special characters from the text based on the following regex

**[^a-zA-Z0-9\s].** Using this regex we get special characters other than alpha numeric characters or spaces. All such special characters are removed from the text.

ii) Tokenizing - For text in each file we first tokenized it into individual words,if they do not belong to the stopword which is checked as mentioned above.

All individual words are converted to their lowercase form and then we stem these words using the PorterStemmer as mentioned above.

iii) Permuterms - After this, we create all possible permuterms of these stemmed words and stored them in the inverted index dictionary along with their set of documents.

For example permuterms for &quot;brutus$&quot; are :

&quot;rutus$b&quot;,&#39;utus$br&#39;,&#39;tus$bru&#39;,&#39;us$brut&#39;,&#39;s$brutu&#39;,&#39;$brutus&#39;

All these permuterms will contain the same set of documents in the dictionary.

**<h2>Querying</h2>**

i) the inputted query is converted to lowercase characters followed by stemming and tokenization similar to what we did while building the inverted index.to handle wildcard query searches,special characters arent removed and words are tokenized here by using the inbuilt split method.

ii) then we classify the query tokens as connecting words(and,or,not) or different words(which are the words other than connecting words).

iii) handling query is carried out with the help of the queue.first connecting word if and/or operates on the first two non connecting words.we passed the posting list of those two non connected words into the queue and processed it with respect to the connector by performing intersection or union of the respective posting list following which the individual posting list is dequeued and the resulting list is then enqueued.

We handled the not operation while traversing the query tokens.This is done by checking if the last added connecting word is &#39;not&#39; and if the last connecting word is not we enque the negation set of the keyword&#39;s posting list.

iv) Handling spelling mistakes in the searched query: We used the dynamic programming approach to find the edit distance between 2 words. We compare all keywords and the one with the minimum distance is used for our search.

v) Wildcard Query handling: For every wildcard query we rotate the words till we get **\*** at the end. Then we search the invertedin index keys so that they have the partial word as their substring and we create a union of all such words.

This gives us the posting list of all the words that satisfies the entry.
