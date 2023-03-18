import pyttsx3
import datetime
import speech_recognition as SR
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import wakeonlan

engine = pyttsx3.init()

# Set up Spotify authentication
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="",
                                               client_secret="",
                                               redirect_uri="http://localhost:8000/callback",
                                               scope="user-read-playback-state,user-modify-playback-state"))


def speak(audio):
    engine.say(audio)
    engine.runAndWait()
    
def time_():
    Time=datetime.datetime.now().strftime("%I:%M:%S") # 12 hr clock
    speak("The time is")
    speak(Time)
    
def date_():
    year = str(datetime.datetime.now().year)
    month = str(datetime.datetime.now().strftime("%B"))
    date = str(datetime.datetime.now().strftime("%d"))
    speak("The date is")
    speak(date)
    speak(month)
    speak(year)
    
def wish_me():
    hour =  datetime.datetime.now().hour
    if hour >=6 and hour<12:
        speak("Good morning sir, Jarvis at your service")
    elif hour>=12 and hour<18:
        speak("Good afternoon sir, Jarvis at your service")
    elif hour>=18 and hour<24:
        speak("Good evening sir, Jarvis at your service")
    else:
        speak("Good night sir, Jarvis at your service")
    
def Take_Command():
    r=SR.Recognizer()
    with SR.Microphone() as source:
        print("Jarvis Listening.........")
        r.pause_threshold = 1 # Wait in listening state for 1 minute
        audio = r.listen(source)
    
    # Try to listen again if jarvis is unable to recognize your request
    try:
        print("Jarvis is recognizing.........")
        query = r.recognize_google(audio, language='en-US')
        print(query)
        
    except Exception as e:
        print(e)
        print("Please repeat that again.........")
        return "None"
    return query

# Define function to play a Spotify track
def play_track(track_name):
    # Search for the track on Spotify
    results = sp.search(q=track_name, type='track', limit=1)
    items = results['tracks']['items']
    if len(items) == 0:
        # If the track wasn't found, tell the user and exit
        engine.say(f"Sorry, I couldn't find the track {track_name} on Spotify.")
        engine.runAndWait()
        return
    track_uri = items[0]['uri']
    # Check if Spotify is already playing
    playback_state = sp.current_playback()
    if playback_state is not None and playback_state['is_playing']:
        # If Spotify is playing, pause it first
        sp.pause_playback()
    # Start playing the track
    sp.start_playback(uris=[track_uri])
    engine.say(f"Playing {items[0]['name']} by {items[0]['artists'][0]['name']}.")
    engine.runAndWait()
    
if __name__ == "__main__":

    while True:
        query = Take_Command().lower()
        # Login, Log out, shutdown, restart the system
        if 'wake up' in query:
            #speak("Welcome back, sir! It's good to see you with a smile on your face today. Just so you know, I've got your back and your data, all your backups have been safely stashed away in the cloud. And, as always, your computer is primed and ready for whatever crazy work schedule you throw at it. Let's show those deadlines who's boss!")
            # password = ""
            # while True:
            #     password_query = Take_Command().lower()
            #     if password_query == password:
            #         speak("Password accepted. It's good to see you again, sir!")
            #         # Send WoL packet to the computer's network card
            #         wakeonlan.send_magic_packet('')
            #         break
            #     else:
            #         speak("Incorrect password. Please try again.")            
            # break
            # Send WoL packet to the computer's network card
            wakeonlan.send_magic_packet('')
            break
        
        elif 'log out the systems' in query:
            wish_me()
            speak("logging out of the systems sir, have a nice day")
            os.system("shutdown -l")
            break

        elif 'restart the systems' in query:
            wish_me()
            speak("Restarting your systems sir, will be back in a moment")
            os.system("shutdown /r /t 1")
            break

        elif 'shutdown the systems' in query:
            wish_me()
            speak("Shutting down your systems sir")
            os.system("shutdown /s /t 1")
            break
            
        elif 'exit' in query:
            speak("Goodbye Sir! Have a nice day")
            exit()

        # Play songs fro spotify
        if 'play songs' in query:
            speak("What song would you like me to play sir!")
            song = Take_Command().lower()
            print(f"You said: ", song)
            if 'play' in song:
                # Extract the track name from the command and play it on Spotify
                track_name = query.replace('play', '').strip()
                play_track(track_name)
        break