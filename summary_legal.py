import re

def summarize(text):
    clean_cont = text.split(".")
    shear = [i.replace('\xe2\x80\x9c', '') for i in clean_cont]
    shear = [i.replace('\xe2\x80\x9d', '') for i in shear]
    shear = [i.replace('\xe2\x80\x99s', '') for i in shear]

    shears = [x for x in shear if x != ' ']
    shearss = [x for x in shears if x != '']
    dubby = [re.sub("[^a-zA-Z]+", " ", s) for s in shearss]

    from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
    from sklearn.decomposition import LatentDirichletAllocation, NMF
    import pandas as pd
    import numpy as np
    from sklearn.feature_extraction.stop_words import ENGLISH_STOP_WORDS
    vect = TfidfVectorizer(ngram_range=(1, 1), stop_words='english')
    dtm = vect.fit_transform(dubby)
    pd.DataFrame(dtm.toarray(), columns=vect.get_feature_names())
    #lda = LatentDirichletAllocation(n_components=5)
    lda = NMF(n_components=5, random_state=1, alpha=.1, l1_ratio=.5, init='nndsvd')
    lda.fit_transform(dtm)
    lda_dtf = lda.fit_transform(dtm)
    import numpy as np
    sorting = np.argsort(lda.components_)[:, ::-1]
    features = np.array(vect.get_feature_names())
    import mglearn
    mglearn.tools.print_topics(topics=range(5), feature_names=features,
                               sorting=sorting, topics_per_chunk=5, n_words=10)
    Agreement_Topic = np.argsort(lda_dtf[:, 2])[::-1]
    for i in Agreement_Topic[:4]:
        print(".".join(dubby[i].split(".")[:2]) + ".\n")

    Domain_Name_Topic = np.argsort(lda_dtf[:, 4])[::-1]
    for i in Domain_Name_Topic[:4]:
        print(".".join(dubby[i].split(".")[:2]) + ".\n")



if __name__ == "__main__":
    file = open("Punctuated.txt","r")
    text = file.read()
    summarize(text)


