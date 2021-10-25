import xml.etree.ElementTree as ET
import json
import os
import nltk
from nltk import jsontags
from nltk.util import pr


if __name__=="__main__":

    # PubmedPath = f'{os.getcwd()}/HW2/pubmed'
    # TweetPath = f'{os.getcwd()}/HW2/twitter'
    # PubmedFiles = os.listdir(PubmedPath)
    # TwitterFiles = os.listdir(TwitterPath)
    # PubmedDoc = {}
    # TwitterDoc = {} 

    # for FileName in PubmedFiles:
    #     tree = ET.parse(f'{PubmedPath}/{FileName}')
    #     for title in tree.iter(tag='ArticleTitle'):
    #         PubmedDoc[title.text] = {}
    # for FileName in TweetFiles:
    #     print(FileName)

    PubmedFile = f'{os.getcwd()}/HW2/pubmed/data0_1000.xml'
    PubmedDoc = {}
    tree = ET.parse(PubmedFile)
    for art in tree.iter(tag = 'Article'):
        Article = {}
        Title = art.find("ArticleTitle").text
        for abs in art.iter(tag = 'Abstract'):    
            for content in abs.iter(tag= 'AbstractText'):
                if 'Label' in content.attrib:
                   Article[content.attrib['Label']] = content.text
                else:
                    if content.text == '':
                        Article[''] = 'No abstract available'
                    else:
                        Article['Abstract'] = content.text
        PubmedDoc[Title] = Article

    with open('PubmedDoc.json','w')as fpick:
        json.dump(PubmedDoc,fpick)