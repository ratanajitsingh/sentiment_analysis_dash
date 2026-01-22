# News Sentiment Analysis Dashboard 
Real time NLP dashboard that analyses news trends and sentiment using **NewsAPI**, **VADAR Sentiment Analysis**, and **Streamlit**

This application fetches live news articles based on topics defined by the user, analyzes their sentiment and visualizes the data through interactive charts and word clouds. 

## Features 

* **Real-time data fetching**: Pulls the latest news articles using NewsAPI.
* **Sentiment Analysis**: Uses **VADER** (Valence Aware Dictionary and sEntiment Reasoner) to score the headlines and descriptions, and is specifically tuned for social media and short text contexts. 
* **Interactive Visualizations**:
  * **Trend Line**: Tracks sentiment fluctuations over the past week and displays it in a line graph. 
  * **Sentiment Distribution**: Colour coded bar charts showing the sentiment of the top 20 articles
  * **Word Cloud**: Visualizes the most frequent keywords used in the current news cycle.
* **Customizable Search**: Has a sidebar to manage the amount of articles and an adjustable date range (1-28 days) 

## Tech Stack
* **Python 3.8**
* **Steamlit** (UI/Dashboard)
* **Pandas** (Data Manipulation)
* **Plotly Express** (Interactive graphing)
* **VADER Sentiment** (NLP)
* **WordCloud and Matplotlib** (keyword visualization)


## Installation and set up 
### 1. clone repository 
    git clone [https://github.com/yourusername/sentiment-analysis-dash.git](https://github.com/yourusername/sentiment-analysis-dash.git)
    cd sentiment_analysis_dash
## 2. install dependencies
    pip install -r requirements.txt
## 3. Get a NewsAPI Key
    1. go to NewsAPI.org 
    2. get a free key
## 4. Configure Environment Vars
    Create a .env file in the root directory and add your api key:
        NEWS_API_KEY = your_api_key_here
## 5. Run the app 
    open the terminal with the right directory and access level 
    run it through : streamlit run src/app.py

## Project Structure 
* **app.py** : Main app script containing the UI layout and the logic
* **requirements.txt** : list of all python dependencies 
* **.env**: not included in repo, stores the API Key

## Screenshots 
<img width="1902" height="1061" alt="Screenshot 2026-01-22 151254" src="https://github.com/user-attachments/assets/8c7e2f33-0517-4a32-9061-9259b7c8282d" />
<img width="1904" height="1070" alt="Screenshot 2026-01-22 151320" src="https://github.com/user-attachments/assets/e9a5adc5-c8b5-44c6-a468-9e8122fab808" />
<img width="1909" height="1072" alt="Screenshot 2026-01-22 151310" src="https://github.com/user-attachments/assets/9a9aa114-cd6d-4a51-88cc-29f3d0c9433f" />


