import pyttsx3
import datetime
import speech_recognition as SR

engine = pyttsx3.init()


def speak(audio):
    engine.say(audio)
    engine.runAndWait()
    
def time_():
    Time=datetime.datetime.now().strftime("%I:%M:%S") # 12 hr clock
    speak("The time is")
    speak(Time)
    
def date_():
    year = str(datetime.datetime.now().year)
    month = str(datetime.datetime.now().month)
    date = str(datetime.datetime.now().day)
    speak("The date is")
    speak(year)
    speak(month)
    speak(date)
    
def wish_me():
    speak("Welcome back sir!")
    time_()
    date_()

    hour =  datetime.datetime.now().hour
    
    if hour >=6 and hour<12:
        speak("Good Morning Sir!")
    elif hour>=12 and hour<18:
        speak("Good Afternoon Sir!")
    elif hour>=18 and hour<24:
        speak("Good Evening Sir!")
    else:
        speak("Good Night Sir!")
    
    speak("Jarvis at your service. How can i help you sir!")
    
def Take_Command():
    r=SR.Recognizer()
    with SR.Microphone() as source:
        print("Jarvis Listening.........")
        r.pause_threshold = 1 # Wait in listening state for 1 min
        audio = r.listen(source)
    
    # Try to listen again if jarvis is unable to recognize your request
    try:
        print("Jarvis is recognizing.........")
        query = r.recognize_google(audio, language='en-US')
        print(query)
        
    except Exception as e:
        print(e)
        print("Please repeat that again.........")
        return query
    
Take_Command()