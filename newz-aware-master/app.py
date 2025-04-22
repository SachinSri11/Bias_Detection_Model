from flask import Flask, render_template
from predictor import predict
import json
import requests
import os
from dotenv import load_dotenv

def get_news():
    load_dotenv()  # Load .env variables
    NEWS_API_KEY=os.getenv('NEWS_API_KEY')
    if not NEWS_API_KEY:
        raise ValueError("NEWS_API_KEY is not set in the environment variables.")

    url=f'https://newsapi.org/v2/top-headlines?country=us&category=politics&apiKey={NEWS_API_KEY}'

    try:
        response=requests.get(url)
        response.raise_for_status()  # Raises HTTPError for bad responses (4xx and 5xx)

        news_data=response.json()

        with open('sampleNews.json', 'w') as f:
            json.dump(news_data, f, indent=4)

        return news_data

    except requests.exceptions.RequestException as e:
        print(f"Error fetching news: {e}")
        return None


    # For testing the app use the code below as sample news to avoid large number of API calls
    # file = open('sampleNews.json', 'r')
    # news = json.load(file)

    # return news



def make_predictions():
    articles = get_news()['articles']
    titles = [article['title'] for article in articles]
    url = [article['url'] for article in articles]
    img = [article['urlToImage'] for article in articles]

    predictions = [predict(title) for title in titles]

    for i,pred in enumerate(predictions):
        if pred == 0:
            predictions[i] = 'Right'

        elif pred == 1:
            predictions[i] = 'Neutral'

        else:
            predictions[i] = 'Left'

    list_of_articles = list(zip(titles, url, img, predictions))

    return list_of_articles



app = Flask(__name__)

@app.route('/')
def index():
    
    list_of_articles = make_predictions()

    return render_template('index.html', articles = list_of_articles)


if __name__ == '__main__':
    app.run()