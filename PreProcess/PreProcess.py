import pickle
import os
import xml.etree.ElementTree as ET

if __name__ == "__main__":
    Path = f'{os.getcwd()}/hw2/Web/pubmed'
    OutPath = f'{os.getcwd()}/hw2/Web/pubmed/pubmed_data.pkl'
    PubmedFiles = os.listdir(Path)
    PubmedDoc = {}
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
    
    # print(len(PubmedDoc))

    with open(OutPath, 'wb')as fpick:
        pickle.dump(PubmedDoc, fpick)