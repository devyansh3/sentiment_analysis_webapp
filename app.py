import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt

st.title("Sentiment analysis of tweets about US Airlines")
st.sidebar.title("Sentiment analysis of tweets about US Airlines")

st.markdown("This application is a Streamlit dashboard to analyze the sentiment of Tweets 🐦")
st.sidebar.markdown("This application is a Streamlit dashboard to analyze the sentiment of Tweets 🐦")

DATA_URL =("C:/Users/HP/OneDrive/Desktop/tweets/Tweets.csv")


@st.cache(persist=True)
def load_data():
    data = pd.read_csv(DATA_URL)
    #using to data and time function of pandas to convert the date and tome columns in the csv file to standardized format
    data['tweet_created'] = pd.to_datetime(data['tweet_created'])
    return data

data = load_data()
# st.write(data)

st.sidebar.subheader("Show random tweet")
#creating a radio buttuon to allow the code to show a random tweet when prompted by the user
#options are passed as tuple 
random_tweet=st.sidebar.radio('choose the sentiment of the tweet', ('positive', 'neutral', 'negative'))
#will the query the twwet data using query function of pandas and display it in the sidebar
st.sidebar.markdown(data.query('airline_sentiment == @random_tweet')[["text"]].sample(n=1).iat[0,0])

#displaying histogram and piechart for tweet data based on sentiment with alowwing the user to choose from which kind of chart to be displayed

st.sidebar.markdown("### Number of tweets by sentiment")
#adding key=1 that will allow us to use slectbox with piechart and histogram once again in the code with key = 2, key is used to differentiate the states of diffent widgets and avoid confusion for streamlit
select = st.sidebar.selectbox('Visualization type', ['Histogram', 'Pie chart'], key='1')
#new dataframe to display the charts with value counts that give the no of tweets with specific sentiment
sentiment_count= data['airline_sentiment'].value_counts()
#write func lets us have a look at the result of the data frame created 
# st.write(sentiment_count)

#creating a clean data frame that will be fed to plotly to plot the charts

sentiment_count = pd.DataFrame({'Sentiment': sentiment_count.index, 'Tweets': sentiment_count.values})

#giving option to hide the plots

if not st.sidebar.checkbox("Hide", True):
    st.markdown('### Number of Tweets by sentiment')
    if select == "Histogram":
        #using sentiment  as x-axis and tweet as y-axis pe values and data frame passed is sentiment_count, bar func is for plotting histogram
        fig = px.bar(sentiment_count, x='Sentiment', y="Tweets", color="Tweets", height =500)
        #displaying the made chart using plotly function
        st.plotly_chart(fig)
    else:
        #using pie function for pie chart now
        fig = px.pie(sentiment_count, names='Sentiment', values="Tweets")
        st.plotly_chart(fig)

# st.sidebar.subheader("When and Where are the users tweeting from?")
# hour=st.sidebar.slider("Hour of the day",0,23)
# modified_data = data[data['tweet_created'].dt.hour == hour]
# if not st.sidebar.checkbox("Close", True, key='2'):
#     st.markdown("### Tweets locations based on the time of the day")
#     st.markdown("%i tweets between %i:00 and %i:00" % (len(modified_data), hour, (hour+1)%24))
#     st.map(modified_data)

# st.sidebar.subheader("Breakdown airline tweets by sentiment")
# #creating multiselect widget allowing user to select how many airlines for which data to be displayed
# choice = st.sidebar.multiselect('Pick airlines', ('US Airways', 'United', 'American', 'Southwest', 'Delta', 'Virgin America'), key ='0')

# #only if user has chosen an airline then only display the histogram , hence lenght of choice has to be greater than 0
# if len(choice) > 0 :
#     # create a data frame that is subset of oroginal data frame and contains data fro only the chosen airlines
#     choice_data = data[data.airline.isin(choice)]

#creating a wordcloud for tweets

st.sidebar.header("Word Cloud")
word_sentiment = st.sidebar.radio('Display word cloud for what sentiment?', ('positive', 'neutral', 'negative'))
if not st.sidebar.checkbox("Close", True, key='4'):
    st.subheader('Word cloud for %s sentiment' % (word_sentiment))
    df = data[data['airline_sentiment']==word_sentiment]
    words = ' '.join(df['text'])
    processed_words = ' '.join([word for word in words.split() if 'http' not in word and not word.startswith('@') and word != 'RT'])
    wordcloud = WordCloud(stopwords=STOPWORDS, background_color='white', width=800, height=640).generate(processed_words)
    plt.imshow(wordcloud)
    plt.xticks([])
    plt.yticks([])
    st.pyplot()
st.set_option('deprecation.showPyplotGlobalUse', False)