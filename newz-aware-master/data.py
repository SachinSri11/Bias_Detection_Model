import spacy
from nltk.corpus import stopwords
import re
       
import requests
from bs4 import BeautifulSoup

class PreProcessor:

    def __init__(self, lang = 'english'):
        self.nlp = spacy.load('en_core_web_sm')
        self.stop_words = set(stopwords.words(lang))

    def remove_special_chars(self, doc):

        doc = " ".join(re.findall(r'[a-zA-Z0-9]+', doc))
        return doc.lower()

    def lemmatize(self, doc):
        doc = self.nlp(doc)
        tokenized = [token.lemma_ for token in doc]
        return tokenized

    def remove_stop_words(self, tokenized_doc):

        tokenized_doc_no_stopwords = []

        for word in tokenized_doc:
            if word not in self.stop_words:
                tokenized_doc_no_stopwords.append(word)

        return tokenized_doc_no_stopwords

    def forward(self, doc):
        doc = self.remove_special_chars(doc)
        doc = self.lemmatize(doc)
        doc = self.remove_stop_words(doc)


        return " ".join(doc)


def scrape_pages(df):
    
    title = []
    body = []
    urls = df['url']

    for i,url in enumerate(urls):

        print(f'On record entry #{i+1}')

        try:
            res = requests.get(url)

        except:
            print('Exception occured')
            title.append('Exception')
            body.append('Exception')

        if res.status_code == 200:
            soup = BeautifulSoup(res.content, 'html.parser')
            try:
                title.append(soup.title.text) 
                body.append(soup.body.text)
            except:
                print('Exception occured')  
                title.append('Exception')
                body.append('Exception')

        else:
            title.append('NULL')
            body.append('NULL')

        
    df['title'] = title 
    df['body'] = body

    return df
