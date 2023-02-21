import eel
import time
from datetime import datetime, timedelta, timezone

eel.init('web')

@eel.expose
def load_modules():
    import pandas
    global pd
    pd = pandas
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
    done = "1"
    eel.go_to('home.html')
    print('load done')
    return done
@eel.expose()
def warningsound():
    sound("audio/danger")
@eel.expose()
def sdestruct(code):
    if code=="5354":
        speak("Warning. Jaguar system engaged")
    else:
        speak("Verification failed")
@eel.expose()
def welcome():
    try:
        f = open('data.txt','r')
        lines=f.readlines()
        name= lines[0]
        gender=lines[2]
        print(gender)
        if name is None:
            speak("Hello. I am Omega, your personal trading assistant")
            speak("Please proceed to settings page to setup Omega")
        else:
            if gender.startswith("Male"):
                speak("Hello sir, welcome back")
            else:
                speak('Hello Madam, welcome back')
    except Exception as e:
        speak(e)
        print(e)
        speak("please proceed to the Settings section to set up the application")
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
try:

    eel.start('index.html', mode='chrome', port=8080, size=(1980,1028))
except Exception as e:
    print(e)