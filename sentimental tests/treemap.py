# libraries for webscraping, parsing and getting stock data
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from yahooquery import Ticker
# for plotting and data manipulation
import pandas as pd
import matplotlib.pyplot as plt
import plotly
import plotly.express as px

# NLTK VADER for sentiment analysis
import nltk
nltk.downloader.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
tickers_dict = {'AMZN': 5, 'TSLA': 1, 'GOOG': 3, 'META': 3, 'KO': 10, 'PEP': 5,  # amazon, tesla, google, meta, coke, pepsi
                'BA': 5, 'XOM': 5, 'CVX': 4, 'UNH': 1, 'JNJ': 3, 'JPM': 3, # boeing, exxon mobil, chevron, united health, johnson&johnson, jp morgan
                'BAC': 5, 'C': 5, 'SPG': 10, 'AAPL': 6, 'MSFT': 5, 'WMT': 6, # bank of america, citigroup, simon property group, apple, microsoft, walmart
                'LMT': 2, 'PFE': 10, 'MMM': 3, 'CRWD': 3, 'WBD': 20, 'DIS': 8, # lockheed martin, pfizer, 3M, crowdstrike, warner bros, disney
                'AIG': 5, 'BRK-B': 4, 'DDOG': 3, 'SLB': 16, 'SONY': 5, 'PLD': 5, # american international group, berkshire hathaway, datadog, schlumberger, sony, prologis
                'INT': 16, 'AMD': 5, 'ISRG': 3, 'INTC': 5} # world fuel services, advanced micro devices, intuitive surgical, intel
tickers = tickers_dict.keys()
number_of_shares = tickers_dict.values()
# Scrape the Date, Time and News Headlines Data
finwiz_url = 'https://finviz.com/quote.ashx?t='
news_tables = {}

for ticker in tickers:
    print(ticker)
    url = finwiz_url + ticker
    req = Request(url=url,headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:20.0) Gecko/20100101 Firefox/20.0'}) 
    response = urlopen(req)    
    # Read the contents of the file into 'html'
    html = BeautifulSoup(response)
    # Find 'news-table' in the Soup and load it into 'news_table'
    news_table = html.find(id='news-table')
    # Add the table to our dictionary
    news_tables[ticker] = news_table

# Parse the Date, Time and News Headlines into a Python List
parsed_news = []
# Iterate through the news
for file_name, news_table in news_tables.items():
    # Iterate through all tr tags in 'news_table'
    for x in news_table.findAll('tr'):
        # read the text from each tr tag into text
        # get text from a only
        text = x.a.get_text() 
        # splite text in the td tag into a list 
        date_scrape = x.td.text.split()
        # if the length of 'date_scrape' is 1, load 'time' as the only element
        if len(date_scrape) == 1:
            time = date_scrape[0]
            
        # else load 'date' as the 1st element and 'time' as the second    
        else:
            date = date_scrape[0]
            time = date_scrape[1]
        # Extract the ticker from the file name, get the string up to the 1st '_'  
        ticker = file_name.split('_')[0]
        
        # Append ticker, date, time and headline as a list to the 'parsed_news' list
        parsed_news.append([ticker, date, time, text])
        
parsed_news[:5] # print first 5 rows of news
# Perform Sentiment Analysis with Vader
# Instantiate the sentiment intensity analyzer
vader = SentimentIntensityAnalyzer()
# Set column names
columns = ['ticker', 'date', 'time', 'headline']
# Convert the parsed_news list into a DataFrame called 'parsed_and_scored_news'
parsed_and_scored_news = pd.DataFrame(parsed_news, columns=columns)

# Iterate through the headlines and get the polarity scores using vader
scores = parsed_and_scored_news['headline'].apply(vader.polarity_scores).tolist()
# Convert the 'scores' list of dicts into a DataFrame
scores_df = pd.DataFrame(scores)

# Join the DataFrames of the news and the list of dicts
parsed_and_scored_news = parsed_and_scored_news.join(scores_df, rsuffix='_right')
# Convert the date column from string to datetime
parsed_and_scored_news['date'] = pd.to_datetime(parsed_and_scored_news.date).dt.date
parsed_and_scored_news.head()
print(parsed_and_scored_news)
# Group by each ticker and get the mean of all sentiment scores
mean_scores = parsed_and_scored_news.groupby(['ticker']).mean()
print(mean_scores)
sectors = []
industries = []
prices = []
print("section2")
for ticker in tickers:
    symbol = ticker
    tkr = Ticker(symbol)
    # Get the regular market price for the symbol
    regular_market_price = tkr.price[symbol]['regularMarketPrice']
    # Get the sector for the symbol
    sector = tkr.asset_profile[symbol]['sector']
    # Get the industry for the symbol
    industry = tkr.asset_profile[symbol]['industry']
    tickerdata= Ticker(symbol)
    print(prices)
    prices.append(regular_market_price)
    sectors.append(sector)
    industries.append(industry)
    print(regular_market_price)
    print(sector)
    print(industry)

# dictionary {'column name': list of values for column} to be converted to dataframe
d = {'Sector': sectors, 'Industry': industries, 'Price': prices, 'No. of Shares': number_of_shares}
# create dataframe from 
df_info = pd.DataFrame(data=d, index = tickers)
df_info['Total Stock Value in Portfolio'] = df_info['Price']*df_info['No. of Shares']
df = mean_scores.join(df_info)
df = df.rename(columns={"compound": "Sentiment Score", "neg": "Negative", "neu": "Neutral", "pos": "Positive"})
df = df.reset_index()
# group data into sectors at the highest level, breaks it down into industry, and then ticker, specified in the 'path' parameter
# the 'values' parameter uses the value of the column to determine the relative size of each box in the chart
# the color of the chart follows the sentiment score
# when the mouse is hovered over each box in the chart, the negative, neutral, positive and overall sentiment scores will all be shown
# the color is red (#ff0000) for negative sentiment scores, black (#000000) for 0 sentiment score and green (#00FF00) for positive sentiment scores

fig = px.treemap(df, path=[px.Constant("Sectors"), 'Sector', 'Industry', 'ticker'], values='Total Stock Value in Portfolio',
                  color='Sentiment Score', hover_data=['Price', 'Negative', 'Neutral', 'Positive', 'Sentiment Score'],
                  color_continuous_scale=['#FF0000', "#000000", '#00FF00'],
                  color_continuous_midpoint=0)

fig.data[0].customdata = df[['Price', 'Negative', 'Neutral', 'Positive', 'Sentiment Score']].round(3) # round to 3 decimal places
fig.data[0].texttemplate = "%{label}<br>%{customdata[4]}"

fig.update_traces(textposition="middle center")
fig.update_layout(margin = dict(t=30, l=10, r=10, b=10), font_size=20)

plotly.offline.plot(fig, filename='stock_sentiment.html', auto_open=False) # this writes the plot into a html file and opens it
