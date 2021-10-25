# ncku_bir_hw2
生醫資訊作業

## Environment
* Python 3.7.11
* Flask
* NLTK

## Data Preprocessing
* 對XML檔案進行處理，避免每次都需重複處理大量文檔
    ```
    for file in PubmedFiles:
        tree = ET.parse(f'{Path}/{file}')
        for art in tree.iter(tag = 'Article'):
            Article = {}
            Title = art.find("ArticleTitle").text
            for abs in art.iter(tag = 'Abstract'):    
                for content in abs.iter(tag= 'AbstractText'):
                    if 'Label' in content.attrib:
                            Article[content.attrib['Label']] = content.text
                    else:
                        Article['Abstract'] = content.text
                PubmedDoc[Title] = Article

    with open(OutPath, 'wb')as fpick:
            pickle.dump(PubmedDoc, fpick)
    ```
* 對tweetpy取得之data，只取需要的內容：user, screen_name, text
    ```
    for tweet in tweets:
        data = {}
        data["name"] = tweet.user.name
        data["screen_name"] = tweet.user.screen_name
        data["text"] = tweet.text
        tweet_data.append(data)
    ```
## Zipf Distribution
* 1000篇文章中，出現頻率最高的前60個字
![](https://i.imgur.com/NONRxNp.png)
* Stemming 去除字尾
![](https://i.imgur.com/z2MFkBa.png)
* 移除Stop Words
![](https://i.imgur.com/9qpBaxR.png)
* 移除Stop Words並去除字尾
![](https://i.imgur.com/bca7PT6.png)
* 除去Stop Words之前，高頻字多為'the'、'is'、'at'、'which'、'on'等功能詞，與文章主題較無關聯。

## Get Twitter Data
* 使用Twitter API取得twitter data

    ```
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=False)

    search_words = ["#covid19", "#covid"]

    tweets = tweepy.Cursor(api.search_tweets,
                           q=search_words,
                           lang="en").items(1000)
    ```
* api.search_tweets 可透過關鍵字取得特定主題之推文
* Requests / 15-min window (app auth) : 450

## NLTK
* NLTK 全名是 Natural Language Tool Kit， 是一套基於 Python 的自然語言處理工具。
* 移除Stop words
    ```
    EngStopWords = set(stopwords.words('english'))
    for word in tqdm(words):
        if word in EngStopWords:
            clean_words.remove(word)
    ```
* Stemming
    ```
    stemmer = PorterStemmer()
    stem_words = [stemmer.stem(word) for word in words]
    ```
## Edit distance
* 計算Edit distance用以找出拼字錯誤或相似字
    ```
    difflib.get_close_matches(KeyWord.lower(), wordList, cutoff=0.7)
    ```
* 存成Dictionary, 用以顯示與搜尋
    ```
    KeyWordList = sorted(KeyWordList.items(), key=lambda d: d[1], reverse=True)
    ```
## Markupsafe
* 保留html tag的功能，用以顯示文章中的關鍵字
    ```
    for word in match_article:
        replaceWord = "<font style =\'background:#78A1BB;\'>"+ word + "</font>"
        newArticle[label] = newArticle[label].replace(word, replaceWord)
    newArticle[label] = Markup(newArticle[label])
    ```
## Reference
* [How to Use Python to Find the Zipf Distribution of a Text File](https://code.tutsplus.com/tutorials/how-to-use-python-to-find-the-zipf-distribution-of-a-text-file--cms-26502)
* [Python深度學習筆記(五)：使用NLTK進行自然語言處理](https://yanwei-liu.medium.com/python%E6%B7%B1%E5%BA%A6%E5%AD%B8%E7%BF%92%E7%AD%86%E8%A8%98-%E4%BA%94-%E4%BD%BF%E7%94%A8nltk%E9%80%B2%E8%A1%8C%E8%87%AA%E7%84%B6%E8%AA%9E%E8%A8%80%E8%99%95%E7%90%86-24fba36f3896)
* [Python | Stemming words with NLTK](https://www.geeksforgeeks.org/python-stemming-words-with-nltk/)
* [Stemming words with NLTK](https://pythonprogramming.net/stemming-nltk-tutorial/)
* [Stemming and Lemmatization in Python](https://www.datacamp.com/community/tutorials/stemming-lemmatization-python)
* [Flask上線](https://minglunwu.github.io/notes/2021/flask_plus_wsgi.html#application-server)
* [Suffix Tree](https://pypi.org/project/suffix-trees/)
* [Python Flask 建立簡單的網頁](https://shengyu7697.github.io/python-flask/)
* [Python Web Flask — GET、POST傳送資料](https://medium.com/seaniap/python-web-flask-get-post傳送資料-2826aeeb0e28)
* [Porter stemming algo](http://snowball.tartarus.org/algorithms/porter/stemmer.html)
