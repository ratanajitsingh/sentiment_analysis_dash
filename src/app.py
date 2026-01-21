import os
import requests
from textblob import TextBlob
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("NEWS_API_KEY")



#fetches the top (size) news articles about a topic of choice
def fetch_news(topic):

    #define the size required
    size = 5
    if not API_KEY:
        return []

    url = f"https://newsapi.org/v2/everything?q={topic}&apiKey={API_KEY}&language=en&sortBy=relevancy&pageSize={size}"
    try:
        response = requests.get(url)
        data = response.json()

        #cehcks to see if the API is running correctly
        if data.get("status") != "ok":
            print(f"Error Alert!: {data.get('message')}")
            return []

        return data.get("articles", [])
    except Exception as error:
        print(f"Failed : {error}")
        return []


# inputs a list of articles and adds a sentiment score to each
def analyze_sentiment(articles):
    analyzed_data = []
    for article in articles:
        title = article.get("title", '')
        description = article.get("description", '') or ''

        # making it a single interactable element
        text = f"{title}\n{description}"

        # using textblob to calculate polarity -1 refers to absolute Negative to +1 refers to absolute Positive
        blob = TextBlob(text)
        sentiment = blob.sentiment.polarity

        analyzed_data.append({
            'title': title,
            'description': description,
            'sentiment': sentiment,
            'url': article['url']
        })


    return analyzed_data

#TESTING

if __name__ == "__main__":
    test_topic = "Elon Musk"
    raw_articles = fetch_news(test_topic)
    results = analyze_sentiment(raw_articles)
    if raw_articles:
        for res in results:
            print(f'\nTitle: {res["title"]}')
            print(f"Sentiment: {res['sentiment']} Positive" if res['sentiment'] > 0 else f"Sentiment: {res['sentiment']} Negative/Neutral")
    else:
        print("No news found, check API key")



