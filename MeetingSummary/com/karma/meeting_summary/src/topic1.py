doc1 = "Sugar is bad to consume. My sister likes to have sugar, but not my father."
doc2 = "My father spends a lot of time driving my sister around to dance practice."
doc3 = "Doctors suggest that driving may cause increased stress and blood pressure."
doc4 = "Sometimes I feel pressure to perform well at school, but my father never seems to drive my sister to do better."
doc5 = "Health experts say that Sugar is not good for your lifestyle."

file = open("text.txt","r")
doc6 = file.read()
# compile documents
#doc_complete = [doc1, doc2, doc3, doc4, doc5]
doc_complete = [doc6]

from nltk.corpus import stopwords 
from nltk.stem.wordnet import WordNetLemmatizer
import string
stop = set(stopwords.words('english'))
exclude = set(string.punctuation) 
lemma = WordNetLemmatizer()
def clean(doc):
    stop_free = " ".join([i for i in doc.lower().split() if i not in stop])
    punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
    normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())
    return normalized

doc_clean = [clean(doc).split() for doc in doc_complete]   

print("#####################")
print (doc_clean)
print("#####################")

# Importing Gensim
import gensim
from gensim import corpora

# Creating the term dictionary of our courpus, where every unique term is assigned an index. 
dictionary = corpora.Dictionary(doc_clean)
#dictionary.filter_extremes(no_below=4)


# Converting list of documents (corpus) into Document Term Matrix using dictionary prepared above.
doc_term_matrix = [dictionary.doc2bow(doc) for doc in doc_clean]

print(doc_term_matrix)

print ([[(dictionary[id], freq) for id, freq in cp] for cp in doc_term_matrix[:1]])

my_dict = {}
for cp in doc_term_matrix[:1]:
   for id, freq in cp:
      my_dict[dictionary[id]] = freq
print("************************************************")
print(my_dict)
print ("************************************************")


filtered_dict = {}
for key,value in my_dict.iteritems():
    if value > 5 and key.isdigit()==False:
        filtered_dict[key] = value

filtered_dict = sorted(filtered_dict.items(), key=lambda x: x[1])
print("*****************************************")
print(filtered_dict)
print("******************************************")
    
# Creating the object for LDA model using gensim library
Lda = gensim.models.ldamodel.LdaModel

# Running and Trainign LDA model on the document term matrix.
ldamodel = Lda(doc_term_matrix, num_topics=1, id2word = dictionary, passes=50)

print(ldamodel.print_topics(num_topics=1, num_words=3))
