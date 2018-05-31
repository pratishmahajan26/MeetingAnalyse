import logging
logging.basicConfig(format="%(asctime)s : %(levelname)s : %(message)s",level=logging.INFO)

#from gensim.summarization import summarizer,keywords
#import pattern3
from summa import keywords, summarizer

file = open("Punctuated.txt", "r")
text = file.read()

print("Keywords:")
print(keywords.keywords(text))

print("Summary")
print(summarizer.summarize(text))



