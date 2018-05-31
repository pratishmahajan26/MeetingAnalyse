from __future__ import division
import datetime, re, sys
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
from nltk.stem.snowball import SnowballStemmer
import math


def tokenize_and_stem(text):
    tokens = [word for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
    filtered_tokens = []
    # filter out any tokens not containing letters (e.g., numeric tokens, raw punctuation)
    for token in tokens:
        if re.search('[a-zA-Z]', token):
            filtered_tokens.append(token)
    stemmer = SnowballStemmer("english")
    stems = [stemmer.stem(t) for t in filtered_tokens]
    fdist = nltk.FreqDist(stems)
    return stems


token_dict = {}
file = open("Punctuated.txt", "r")
text = file.read()
token_dict["Topic"] =  text
#for article in reuters.fileids():
 #   token_dict[article] = reuters.raw(article)

tfidf = TfidfVectorizer(tokenizer=tokenize_and_stem, stop_words='english', decode_error='ignore')
print 'building term-document matrix... [process started: ' + str(datetime.datetime.now()) + ']'
sys.stdout.flush()

tdm = tfidf.fit_transform(token_dict.values())  # this can take some time (about 60 seconds on my machine)
print 'done! [process finished: ' + str(datetime.datetime.now()) + ']'

from random import randint

feature_names = tfidf.get_feature_names()
print 'TDM contains ' + str(len(feature_names)) + ' terms and ' + str(tdm.shape[0]) + ' documents'

print 'first term: ' + feature_names[0]
print 'last term: ' + feature_names[len(feature_names) - 1]

for i in range(0, 4):
    print 'random term: ' + feature_names[randint(1,len(feature_names) - 2)]



article_id = randint(0, tdm.shape[0] - 1)
#article_text = reuters.raw(reuters.fileids()[article_id])
article_text = text

sent_scores = []
for sentence in nltk.sent_tokenize(article_text):
    score = 0
    sent_tokens = tokenize_and_stem(sentence)
    for token in (t for t in sent_tokens if t in feature_names):
        score += tdm[article_id, feature_names.index(token)]
    sent_scores.append((score / len(sent_tokens), sentence))

summary_length = int(math.ceil(len(sent_scores) / 5))
sent_scores.sort(key=lambda sent: sent[0])

print '*** SUMMARY ***'
for summary_sentence in sent_scores[:summary_length]:
    print summary_sentence[1]

print '\n*** ORIGINAL ***'
print article_text