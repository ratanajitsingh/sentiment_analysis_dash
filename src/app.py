import os
import requests
from textblob import TextBlob
from dotenv import load_dotenv
from datetime import datetime, timedelta
import streamlit as st
import plotly.express as px
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS


load_dotenv()
API_KEY = os.getenv("NEWS_API_KEY")



#fetches the top (size) news articles about a topic of choice
def fetch_news(topic, days, limit):

    #creating a buffer for incomplete data
    buffer = limit
    #define the size required


    #this makes sure that it takes in from the last 7 days
    start_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
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

        return valid_articles[:limit]
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

    #settings config
    st.sidebar.header("Analysis Settings")

    days_choice = st.sidebar.slider(
        "Days to look back",
        min_value =1,
        max_value =28,
        value = 7,
        help = "How far back do you want to search for news?"
    )

    limit_choice = st.sidebar.slider(
        "Maximum number of articles to analyze",
        min_value = 10,
        max_value = 100,
        value = 50,
        step =10,
        help = "How many articles do you want to analyze? (more articles means a longer processing time)."
    )

    st.sidebar.markdown("---")
    st.sidebar.info("Adjust the settings to the analysis to refine search results.")

    #main page

    st.title("News Sentiment Analysis")
    st.write("Enter a topic of interest to see the latest sentiment trends.")

    col1, col2 = st.columns([3,1])
    with col1:
        topic = st.text_input("Search", "Artificial Intelligence")
    with col2:
        st.write("")
        st.write("")

    if st.button("Analyze Sentiment"):
        with st.spinner("Analyzing Sentiment..."):
            raw_articles = fetch_news(topic, days_choice, limit_choice)

        #main statistic
        if raw_articles:
            result = analyze_sentiment(raw_articles)

            df = pd.DataFrame(result)

            #normalising and converting into datetime object
            df['date'] = pd.to_datetime(df['date']).dt.date

            avg_sent = df['sentiment'].mean()


            m_col1, m_col2, m_col3 = st.columns(3)
            with m_col1:
                st.metric("Amount of articles analyzed", len(result))
            with m_col2:
                sentiment_color = "normal"
                if avg_sent > 0.1: sentiment_color = "off"
                st.metric("Average Sentiment", f"{avg_sent:.2f}")
            with m_col3:
                st.metric("TimeFrame", f"Last {days_choice} days")

            st.markdown("---")

            #line graph
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


            #bar graph
            st.subheader("Sentiment Distribution")
            top_n = min(20, limit_choice)
            top_df = df.head(top_n)
            #the bar chart showing individual sentiments
            figure = px.bar(top_df, x = 'title', y = 'sentiment',
                            color = "sentiment",
                            range_y = [-1,1],
                            color_continuous_scale = px.colors.diverging.RdBu,
                            title = f"Sentiment for top articles on '{topic}'")
            st.plotly_chart(figure, use_container_width=True)

            #word cloud section
            st.subheader("Frequent Keywords")

            #creating big string
            text_combined = " ".join(title for title in df.title)

            #creating the word cloud object, also removing the topic itself from the cloud
            custom_sws = set(STOPWORDS)
            custom_sws.add(topic.lower())

            wordcloud = WordCloud(
                width = 800,
                height = 800,
                background_color = "black",
                stopwords = custom_sws,
                colormap= 'viridis',
            ).generate(text_combined)

            fig,ax = plt.subplots(figsize=(10,5))
            ax.imshow(wordcloud, interpolation = 'bilinear')
            ax.axis("off")
            st.pyplot(fig)

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






