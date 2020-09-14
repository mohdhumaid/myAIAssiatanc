import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import smtplib
import webbrowser as wb
import psutil
import pyjokes
import os
import pyautogui
import random
import json
import requests
from urllib.request import urlopen
import wolframalpha
import time

engine = pyttsx3.init()

wolframalpha_app_id = 'place_here' #get new one at https://products.wolframalpha.com/api/

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def time_():
    Time = datetime.datetime.now().strftime("%H:%M:%S") #for 12 hour -%I and for 24 hour- %H
    speak("The current time")
    speak(Time)

def date_():
    year = datetime.datetime.now().year
    month = datetime.datetime.now().month
    date = datetime.datetime.now().day
    speak('The current date is')
    speak(date)
    speak(month)
    speak(year)
def wishme():
    speak('welcome back humaid!')
#    time_()
#    date_()
    hour = datetime.datetime.now().hour
    if hour>=6 and hour<12:
        speak('Good morning HUMAID!')
    elif hour>=12 and hour<18:
        speak('Good afternoon HUMAID!')
    elif hour>=18 and hour<24:
        speak('Good evening HUMAID!')
    else:
        speak('Good night HUMAID!')
    speak('JAR at your saervice my lord. Please tell me how can I help you today')

def TakeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening.....')
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print('Recognition.....')
        query = r.recognize_google(audio,language='en-US')
        print(query)
    except Exception as e:
        print(e)
        print('Say that again please....')
        return "None"
    return query

def sendEmail(to,content):
    server=smtplib.SMTP('smtp.gmail.com',587)
    server.ehlo()
    server.starttls()
    mail = input("Enter mail id:'")
    password = input('Enter password:')
    server.login(mail,password)
    server.sendmail(mail,to,content)

def screenshot():
    img = pyautogui.screenshot()
    img.save('D:/python-file/screenshot.png')
def cpu():
    usage = str(psutil.cpu_percent())
    speak('CPU is at'+usage)
    battery = psutil.sensors_battery()
    speak('Battery is at')
    speak(battery.percent)

def joke():
    speak(pyjokes.get_joke())


if __name__== "__main__":
    speak('JAR at your saervice Sir!!!. Please tell me how can I help you today')
    while True: 
        query = TakeCommand().lower()#take input in lower case
        if 'time' in query:
            time_()
        elif 'date' in query:
            date_()
        elif 'wikipedia' in query:
            speak('searching.....')
            query=query.replace('wikipedia','')
            result=wikipedia.summary(query,sentences=3) 
            speak('According to wikipedia')
            print(result)
            speak(result)
        elif 'send email' in query:
            try:
                speak('what should i say!')
                content=TakeCommand()
                speak('who is the reciever')
                rerciever=input('Enter reciever email:')
                to = rerciever
                sendEmail(to,content)
                speak(content)
                speak('Email has been set!')
            except Exception as e:
                print(e)
                speak('Unable to send!!!')

        elif 'wish me' in query:
            wishme()
        
        elif 'search in chrome' in query:
            speak('what should i search!!')
            chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
            search1 = TakeCommand().lower()
            wb.get(chrome_path).open_new_tab(search1+'.com')
        
        elif 'search youtube' in query:
            speak("What should i search?! my lord!!")
            search_term = TakeCommand().lower()
            speak("Here we goto YOUTUBE!!!!")
            wb.open('https://www.youtube.com/results?search_query='+search_term)
        
        elif 'search google' in query:
            speak("What should i search?! my lord!!")
            search_term = TakeCommand().lower()
            speak("Searching.......")
            wb.open('https://www.google.com/search?q='+search_term)

        elif 'cpu' in query:
            cpu()

        elif 'joke' in query:
            joke()
        
        elif 'go offline' in query:
            speak('GOING Offline SIR!!')
            quit()
        
        elif 'word' in query:
            speak('Opening MS word')
            ms_word = r'C:/Program Files (x86)/Microsoft Office/Office12/WINWORD.EXE'
            os.startfile(ms_word)

        elif 'write a note' in query or 'make a note' in query:
            speak('What should I write sir!!')
            notes = TakeCommand()
            file = open('notes.txt','w')
            speak('Sir should I include date and time!!')
            ans = TakeCommand()
            if 'yes' in ans or 'sure' in ans:
                strTime = datetime.datetime.now().strftime("%H:%M:%S")
                file.write(strTime)
                file.write(':-')
                file.write(notes)
            else:
                file.write(notes)
            speak('Done Taking Notes')

        elif 'show note' in query:
            speak('showing notes')
            file = open('notes.txt','r')
            print(file.read())
            speak(file.read())
        
        elif 'screenshot' in query:
            screenshot()

        elif 'play music' in query:
            songs_dir = 'E:/Music'
            music = os.listdir(songs_dir)
            speak('What should I play?')
            speak('select a number.....')
            ans = TakeCommand().lower()
            while('number' not in ans and ans != 'random' and ans != 'you choose'):
                speak('I could not understand you. Please try again!!')
                ans = TakeCommand().lower()
            if 'number' in ans:
                no = int(ans.replace('number',''))
            elif 'random' or 'you choose' in ans:
                no = random.randint(1,25)
            os.startfile(os.path.join(songs_dir,music[no]))
        elif 'remember that' in query:
            speak("What should I remember?")
            memory = TakeCommand()
            speak("You asked me to remember that"+memory)
            remember = open('memory.txt','w')
            remember.write(memory)
            remember.close()
        elif 'do you remember anything' in query:
            remember = open('memory.txt','r')
            speak('You asked me to remember that'+remember.read())

        elif 'where is' in query:
            query = query.replace("where is","")
            location = query
            speak("User aske to locate"+location)
            wb.open_new_tab("https://www.google.com/maps/place/"+location)
        elif 'news' in query:
            try:
                jsonObj = urlopen("http://newsapi.org/v2/top-headlines?country=us&category=business&apiKey=") #get new api at https://newsapi.org/
                data = json.load(jsonObj)
                i=1

                speak('Here are some top headlines from the Entertainment Idustry')
                print('=================TOP HEADLINES==============='+'\n')
                for item in data['articles']:
                    print(str(i)+'. '+item['title']+'\n')
                    print(item['description']+'\n')
                    speak(item['title'])
                    i += 1
            except Exception as e:
                print(str(e))

        elif 'calculate' in query:
            client = wolframalpha.Client(wolframalpha_app_id)
            indx = query.lower().split().index('calculate')
            query = query.split()[indx + 1:]
            res = client.query(''.join(query))
            answer = next(res.results).text
            print('The Answer is : '+answer)
            speak('The answer is'+answer)

        elif 'what is' in query or 'who is' in query:
            client = wolframalpha.Client(wolframalpha_app_id)
            res = client.query(query)

            try:
                print(next(res.results).text)
                speak(next(res.results).text)
            except StopIteration:
                print('No result')
        elif 'stop listening' in query or 'go sleep' in query:
            speak('For how much second you want to stop listening your command')
            ans = int(TakeCommand())
            time.sleep(ans)
            print(ans)
        elif 'log out' in query:
            os.system("shutdown -l")
        elif 'restart' in query:
            os.system("stutdown /r /t 1")
        elif 'shutdown' in query:
            os.system("shutdown /s /t 1")