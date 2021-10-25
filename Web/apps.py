from flask import Flask
from flask import render_template
from flask import request
import xml.etree.ElementTree as ET
import os
import pickle
import nltk
import difflib
import re
import json
from markupsafe import Markup

app = Flask(__name__)

def search_xml():
    path = f'{os.getcwd()}/content/pubmed_data.pkl'
    with open(path, 'rb')as fpick:
        PubmedDoc = pickle.load(fpick)
    if request.method == "POST" and request.form["Search"]!="":
        KeyWord = request.form["Search"]
        find = []
        index = 0
        for title, article in PubmedDoc.items():
            for label, part in article.items():
                if type(part) == type(''):
                    wordList = re.sub(r"[()\"\[#\]/@;:<>{}`+=~|.!?,…\n\xa0]",'',part).lower().split(" ")
                    find.extend(difflib.get_close_matches(KeyWord.lower(), wordList, cutoff=0.7))
        KeyWordList = dict((word, find.count(word)) for word in set(find))
        KeyWordList = sorted(KeyWordList.items(), key=lambda d: d[1], reverse=True)
        Pubmed_Search_List = get_search_xml(KeyWordList,PubmedDoc)
        return render_template('search_pm.html', KeyWordList = KeyWordList, Search = KeyWord, Pubmed_Search_List = Pubmed_Search_List)
    else:
        return render_template('index.html', PubmedDoc = PubmedDoc)

def search_json():
    path = f'{os.getcwd()}/content/data0_1000.json'
    with open(path, 'rb')as fjson:
        TweetDoc = json.load(fjson)
    if request.method == "POST" and request.form["Search"]!="":
        KeyWord = request.form["Search"]
        find = []
        for tweet in TweetDoc:
            wordList = re.sub(r"[()\"#/@;:<>{}`+=~|.!?,…\n\xa0]",'',tweet["text"]).lower().split(" ")
            find.extend(difflib.get_close_matches(KeyWord.lower(), wordList, cutoff=0.7))
        KeyWordList = dict((word, find.count(word)) for word in set(find))
        KeyWordList = sorted(KeyWordList.items(), key=lambda d: d[1], reverse=True)
        KeyWordList, Tweet_Search_List = get_search_json(KeyWordList, TweetDoc)
        return render_template('search_tw.html', KeyWordList = KeyWordList, Search = KeyWord, Tweet_Search_List = Tweet_Search_List)
    else:
        return render_template('twitter.html', TweetDoc = TweetDoc)

def get_search_xml(KeyWordList, PubmedDoc):
    Pubmed_Search_List = []
    new_KeyWordList = []

    for keyword in KeyWordList:
        pattern = re.compile(keyword[0], re.I)
        result = {}
        for title, article in PubmedDoc.items():
            find  = False
            newArticle = article.copy()
            for label, content in article.items():
                if content:
                    match_article = pattern.findall(content)
                    if len(match_article) != 0:
                        find = True
                        for word in match_article:
                            replaceWord = "<font style =\'background:#78A1BB;\'>"+ word + "</font>"
                            newArticle[label] = newArticle[label].replace(word, replaceWord)
                        newArticle[label] = Markup(newArticle[label]) 
            if find:
                match_article = pattern.findall(title)
                newTitle = title
                for word in match_article:
                   replaceWord = "<font style =\'background:#78A1BB;\'>"+ word + "</font>"
                   newTitle = newTitle.replace(word, replaceWord)
                result[Markup(newTitle)] = newArticle
        Pubmed_Search_List.append(result) 

    return Pubmed_Search_List

def get_search_json(KeyWordList, TweetDoc):
    Tweet_Search_List = []
    new_KeyWordList = []

    for keyword in KeyWordList:
        pattern = re.compile(keyword[0], re.I)
        result = []
        for tweet in TweetDoc:
            match_article = pattern.findall(tweet["text"])
            if match_article:
                newTweet = tweet.copy()
                for word in match_article:
                    replaceWord = "<font style =\'background:#78A1BB;\'>"+ word + "</font>"
                    newTweet["text"] = newTweet["text"].replace(word, replaceWord)
                newTweet["text"] = Markup(newTweet["text"])
                result.append(newTweet)
        if len(result) != 0:
            Tweet_Search_List.append(result)
            new_KeyWordList.append(keyword)

    return new_KeyWordList, Tweet_Search_List

@app.route('/', methods=['POST','GET'])
def index():
    path = f'{os.getcwd()}/content/pubmed.pkl'
    with open(path, 'rb')as fpick:
        PubmedDoc = pickle.load(fpick)

    with open(path, 'wb')as fpick:
        pickle.dump(PubmedDoc, fpick)
    return render_template('index.html', PubmedDoc = PubmedDoc)

@app.route('/pubmed', methods=['POST','GET'])
def pubmed():
    return search_xml()

@app.route('/twitter', methods=['POST','GET'])
def twitter():
    return search_json()

@app.route('/zipf')
def zipf():
    return render_template('zipf.html')


if __name__ == '__main__':
    app.debug = True
    app.run()
    # app.run(host='0.0.0.0', port=5001)