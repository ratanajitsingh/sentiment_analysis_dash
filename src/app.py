import os
import requests
from textblob import TextBlob
from dotenv import load_dotenv
from datetime import datetime, timedelta
import streamlit as st
import plotly.express as px
import pandas as pd
import matplotlib.pyplot as plt
from wordcload import WordCloud, STOPWORDS


load_dotenv()
API_KEY = os.getenv("NEWS_API_KEY")



#fetches the top (size) news articles about a topic of choice
def fetch_news(topic):

    #creating a buffer for incomplete data
    buffer = 100
    #define the size required
    size = 100

    #this makes sure that it takes in from the last 7 days
    start_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
    if not API_KEY:
        return []

    url = f"https://newsapi.org/v2/everything?q={topic}&apiKey={API_KEY}&language=en&from={start_date}&sortBy=relevancy&pageSize={buffer}"
    try:
        response = requests.get(url)
        data = response.json()

        #cehcks to see if the API is running correctly
        if data.get("status") != "ok":
            print(f"Error Alert!: {data.get('message')}")
            return []

        all_articles = data.get("articles", [])

        #filtering, with the current API sites some news sites such as CNN become redacted, so removing incomplete data
        valid_articles = []
        for art in all_articles:
            if art.get("title") and art["title"] != "[Removed]":
                valid_articles.append(art)

        return valid_articles[:size]
    except Exception as error:
        print(f"Failed : {error}")
        return []


# inputs a list of articles and adds a sentiment score to each
def analyze_sentiment(articles):
    analyzed_data = []
    for article in articles:
        title = article.get("title", '')
        description = article.get("description", '') or ''
        date_str = article.get("publishedAt", '')

        # making it a single interactable element
        text = f"{title}\n{description}"

        # using textblob to calculate polarity -1 refers to absolute Negative to +1 refers to absolute Positive
        blob = TextBlob(text)
        sentiment = blob.sentiment.polarity

        source_name = article.get("source", "").get('name', 'Unknown Source')

        analyzed_data.append({
            'title': title,
            'source': source_name,
            'sentiment': sentiment,
            'url': article['url'],
            'date': date_str,
        })


    return analyzed_data

#app and UI creation
def main():
    st.set_page_config(page_title="Sentiment Analysis", page_icon="📑")

    st.title("News Sentiment Analysis")
    st.write("Enter a topic of interest to see the latest sentiment trends.")

    #search
    topic = st.text_input("Search", "Artificial Intelligence")

    if st.button("Analyze Sentiment"):
        with st.spinner("Analyzing Sentiment..."):
            raw_articles = fetch_news(topic)

        #main statistic
        if raw_articles:
            result = analyze_sentiment(raw_articles)

            df = pd.DataFrame(result)

            #normalising and converting into datetime object
            df['date'] = pd.to_datetime(df['date']).dt.date

            avg_sent = df['sentiment'].mean()


            col1, col2 = st.columns(2)
            with col1:
                st.metric("Amount of articles analyzed", len(result))
            with col2:
                sentiment_color = "normal"
                if avg_sent > 0.1: sentiment_color = "off"
                st.metric("Average Sentiment", f"{avg_sent:.2f}")

            st.markdown("---")

            st.subheader("Weekly Sentiment Trend")

            daily_trend = df.groupby('date')['sentiment'].mean().reset_index()

            daily_trend = daily_trend.sort_values('date')

            line_fig = px.line(
                daily_trend,
                x="date",
                y="sentiment",
                markers=True,
                title = f"Average daily Sentiment for '{topic}' for the past week",
                labels = {'date': 'Date', 'sentiment': 'Average Sentiment'},
                range_y = [-1, 1]
            )

            line_fig.add_hline(y = 0, line_dash = "dash", line_color = "gray", annotation_text = "Neutral")

            st.plotly_chart(line_fig, use_container_width=True)

            st.subheader("Sentiment Distribution")
            top_df = df.head(20)
            #the bar chart showing individual sentiments
            figure = px.bar(top_df, x = 'title', y = 'sentiment',
                            color = "sentiment",
                            range_y = [-1,1],
                            color_continuous_scale = px.colors.diverging.RdBu,
                            title = f"Sentiment for top articles on '{topic}'")
            st.plotly_chart(figure, use_container_width=True)

            #individual articles
            st.subheader("Top 10 Articles")

            for index, res in df.head(10).iterrows():
                with st.expander(f"{res['source']} - {res['title'][:60]}..."):
                    st.write(f"**Date:**{res['date']}")
                    st.write(f"**Sentiment Score:**{res['sentiment']:.2f}")
                    st.write(f"[Read Full article]({res['url']}")
        else:
            st.warning("No articles found, switch topic or make it broader")


if __name__ == "__main__":
    main()






