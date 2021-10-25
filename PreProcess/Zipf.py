import json
import pickle
import re 
import xml.etree.ElementTree as ET
import os
from operator import itemgetter
import matplotlib.pyplot as plt
import nltk
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from tqdm import tqdm

if __name__ == "__main__":
    # path = f'{os.getcwd()}/HW2/Web/content/pubmed_data.pkl'
    # with open(path, 'rb')as fpick:
    #     PubmedDoc = pickle.load(fpick)
    # FullText = ''
    # art_num = 0
    # for article in PubmedDoc.values():
    #     if art_num > 10000:
    #         break
    #     else:
    #         art_num += 1
    #         for content in article.values():
    #             if type(content) == type(''):
    #                     FullText += content
    path = f'{os.getcwd()}/HW2/Web/content/data0_1000.json'    
    with open(path, 'r')as fjson:
        Tweet = json.load(fjson)
    FullText = ''
    for tw in Tweet:
        FullText += tw["text"]

    frequency = {}
    words = re.sub(r"[()\"#/@;:<>{}`+=~|.!?,\[\]\n\xa0…　]",'',FullText).split()
    stemmer = PorterStemmer()
    
    clean_words = words[:]
    EngStopWords = set(stopwords.words('english'))
    for word in tqdm(words):
        if word in EngStopWords:
            clean_words.remove(word)
    stem_words = [stemmer.stem(word) for word in words]

    freq = nltk.FreqDist(words)
    freq_stem = nltk.FreqDist(stem_words)
    
    freq.plot(60, cumulative=False)
    freq_stem.plot(60, cumulative=False)