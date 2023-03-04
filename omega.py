import eel
import datetime
from datetime import datetime,time
eel.init('web')

@eel.expose
def load_modules():
    import pandas
    global pd
    pd = pandas
    from urllib.request import urlopen, Request
    from sklearn.linear_model import LinearRegression
    global LinearReg
    LinearReg= LinearRegression
    from sklearn.model_selection import train_test_split
    global ttsplit
    ttsplit= train_test_split
    import yfinance
    global yf
    yf=yfinance
    from playsound import playsound
    global sound
    sound=playsound
    import psutil
    global ps
    ps = psutil
    import requests
    global rqs
    rqs = requests
    from bs4 import BeautifulSoup
    global bs
    bs = BeautifulSoup
    def treemap():
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

        plotly.offline.plot(fig, filename='web/stock_sentiment.html', auto_open=False) # this writes the plot into a html file and opens it
    treemap()
    
    import pyttsx3
    global speak
    def pyttsx(audio):
        engine = pyttsx3.init()
        engine.setProperty("volume", 1)
        engine.setProperty('voice','com.apple.speech.synthesis.voice.fiona')
        engine.setProperty('rate',180)
        engine.say(audio)
        engine.runAndWait()
    speak=pyttsx
    global sentimental
    def sentimental_analysis(tickers):
        print(tickers)
        finwiz_url = 'https://finviz.com/quote.ashx?t='
        from nltk.sentiment.vader import SentimentIntensityAnalyzer
        import matplotlib.pyplot as plt
        news_tables = {}
        tickers = ['AMZN', 'TSLA', 'GOOG']
        #tickers = tickers
        #tickers =tickers[1:-1].split(',')

        for ticker in tickers:
            url = finwiz_url + ticker
            req = Request(url=url,headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:20.0) Gecko/20100101 Firefox/20.0'}) 
            response = urlopen(req)    
            # Read the contents of the file into 'html'
            html = BeautifulSoup(response)
            # Find 'news-table' in the Soup and load it into 'news_table'
            news_table = html.find(id='news-table')
            # Add the table to our dictionary
            news_tables[ticker] = news_table
        # Read one single day of headlines for 'AMZN' 
        amzn = news_tables['AMZN']
        # Get all the table rows tagged in HTML with <tr> into 'amzn_tr'
        amzn_tr = amzn.findAll('tr')

        for i, table_row in enumerate(amzn_tr):
            # Read the text of the element 'a' into 'link_text'
            a_text = table_row.a.text
            # Read the text of the element 'td' into 'data_text'
            td_text = table_row.td.text
            # Print the contents of 'link_text' and 'data_text' 
            print(a_text)
            print(td_text)
            # Exit after printing 4 rows of data
            if i == 3:
                break

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
                
        print(parsed_news)
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


        plt.rcParams.update({
            "lines.color": "blue",
            "patch.edgecolor": "blue",
            "text.color": "lightblue",
            "axes.facecolor": "black",
            "axes.edgecolor": "lightgray",
            "axes.labelcolor": "blue",
            "xtick.color": "lightblue",
            "ytick.color": "lightblue",
            "grid.color": "lightblue",

            "savefig.facecolor": "black",
            "savefig.edgecolor": "black"})

        ##############################################
        plt.rcParams['figure.figsize'] = [10, 6]

        # Group by date and ticker columns from scored_news and calculate the mean
        mean_scores = parsed_and_scored_news.groupby(['ticker','date']).mean()

        # Unstack the column ticker
        mean_scores = mean_scores.unstack()

        # Get the cross-section of compound in the 'columns' axis
        mean_scores = mean_scores.xs('compound', axis="columns").transpose()

        # Plot a bar chart with pandas
        mean_scores.plot(kind = 'bar')
        plt.grid()

        plt.savefig('web/my_plot.png')
    sentimental = sentimental_analysis
    import pytz
    global timezones
    timezones = pytz
    import holidays
    global hols
    hols = holidays
    done = "1"
    eel.go_to('home.html')
    print('load done')
    return done
@eel.expose()
def sentiment(ticker):
    speak("loading.")
    sentimental(ticker)
@eel.expose()
def marketstatus():
    from datetime import datetime,time
    import datetime
    new_york_tz = datetime.timezone(datetime.timedelta(hours=-5), name='America/New York')
    now = datetime.datetime.now(new_york_tz).time()
    start_time=time(9,30,0)
    end_time= time(16,0,0)
    today= datetime.datetime.today()
    weekday = today.weekday()
    if weekday<6:
        if start_time <=now <=end_time:
            status="OPEN"
            return status
        else:
            status ="CLOSED"
            return status
    else:
        status="CLOSED"
        return status
@eel.expose()
def marketstatus1():
    from datetime import datetime, time
    import datetime
    hong_kong_tz = datetime.timezone(datetime.timedelta(hours=8), name='Asia/Hong_Kong')
    now = datetime.datetime.now(hong_kong_tz).time()
    start_time=time(9,30,0)
    end_time= time(16,0,0)
    today= datetime.datetime.today()
    weekday = today.weekday()
    if weekday<6:
        if start_time <=now <=end_time:
            status="OPEN"
            return status
        else:
            status ="CLOSED"
            return status
    else:
        status="CLOSED"
        return status
@eel.expose()
def warningsound():
    print("warning sound")
    sound("audio/danger")
@eel.expose()
def welcome():
    try:
        f = open('data.txt','r')
        lines=f.readlines()
        name= lines[0]
        gender=lines[2]
        print(gender)
        if gender.startswith("Male"):
            speak("Hello sir, welcome back")
        else:
            speak('Hello Madam, welcome back')
    except Exception as e:
        speak("Hello. I am Omega, your personal trading assistant")
        speak("Please proceed to settings page to setup Omega")
@eel.expose
def checkram():
    memory_info=ps.virtual_memory()
    current_ram = "Ram: " + str(memory_info.percent)+"%"
    #uncomment to print and debug
    #print(current_ram)
    return current_ram
@eel.expose
def checkcpu():
    cpustat= ps.cpu_percent()
    current_cpu= "CPU: " + str(cpustat)+"%"
    return current_cpu
@eel.expose
def checknetwork1():
    checknetwork= ps.sensors_battery().percent
    checknetwork= str(checknetwork)
    current_network="Battery: " + checknetwork + "%"
    return current_network
@eel.expose
def checkDOJI():
    url = 'https://markets.businessinsider.com/index/dow_jones'
    page = rqs.get(url)

    soup = bs(page.content, 'html.parser')
    index_value = soup.find('span', {'class': 'price-section__current-value'}).text
    index_change = soup.find('span', {'class': 'price-section__absolute-value'}).text.strip()
    index_percent_change = soup.find('span', {'class': 'price-section__relative-value '}).text.strip()
    DOJI= str("DJIA: $"+ index_value + (index_change) + "(" + index_percent_change + "%)")
    return DOJI

@eel.expose
def hktime():
    import datetime
    hong_kong_tz= datetime.timezone(datetime.timedelta(hours=8))
    hong_kong_tz= datetime.datetime.now(hong_kong_tz)
    hong_kong_tz=hong_kong_tz.time()
    hong_kong_tz=hong_kong_tz.strftime("%H:%M:%S")
    hong_kong_tz=str(hong_kong_tz) + " (GMT +8)"
    return hong_kong_tz
@eel.expose
def nytime():
    import datetime 
    new_york_tz= datetime.timezone(datetime.timedelta(hours=-5))
    new_york_tz=datetime.datetime.now(new_york_tz)
    new_york_tz=new_york_tz.time()
    new_york_tz=new_york_tz.strftime("%H:%M:%S")
    new_york_tz=new_york_tz + " (GMT -5)"
    return new_york_tz

@eel.expose
def sentimental_treemap():
    import webbrowser
    webbrowser.open('stock_sentiment.html', new=2)

@eel.expose
def usersettingwrite(username, usercity, user_gender, userdob):
    try:       
        open("data.txt", "w").close()
        with open('data.txt', 'w', encoding='utf-8') as f:
            print("Name: " + username)
            print("Usercity: " + usercity)
            print("usergender: " + user_gender)
            speak("Please wait while we load your data")
            f.write(username)
            f.write('\n')
            f.write(usercity)
            f.write('\n')
            f.write(user_gender)
            f.write('\n')
            f.write(userdob)
            f.close()
            #notifies the user that 
            speak("Data loaded and confirmed. Thank you")
    except Exception as e:
        print(e)


eel.start('index.html', mode='chrome', size=(1980,1028),cmdline_args=['--start-fullscreen'])