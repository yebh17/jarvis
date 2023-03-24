import datetime
import sounddevice as sd
import numpy as np
import speech_recognition as SR
import os
import pyttsx3
from wakeonlan import send_magic_packet
import requests
import pyaudio

engine = pyttsx3.init()

# Get the list of available voices
voices = engine.getProperty('voices')

# Iterate through the available voices and set the preferred voice
for voice in voices:
    if "english" in voice.languages[0] and "f" in voice.gender:
        engine.setProperty('voice', voice.id)
        break

# Set the speech rate (optional)
engine.setProperty('rate', 150)  # Adjust the speech rate as needed

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
        
def wake_up(mac_address):
    send_magic_packet(mac_address)

hass_url = "hass-domain"
entity_id_led = "light.super_galaxy"
entity_id_hall_sofa = "light.hall_sofa"
entity_id_hall_tv = "light.hall_tv"
api_token = "home-assistant-api-token"

def toggle_light_led(hass_url, entity_id_led, api_token):
    url = f"{hass_url}/api/services/light/toggle"
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }
    data = {"entity_id": entity_id_led}
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        print("Successfully toggled the light")
    else:
        print("Failed to toggle the light")
        
def toggle_light_hall_sofa(hass_url, entity_id_hall_sofa, api_token):
    url = f"{hass_url}/api/services/light/toggle"
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }
    data = {"entity_id": entity_id_hall_sofa}
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        print("Successfully toggled the light")
    else:
        print("Failed to toggle the light")
        
def toggle_light_hall_tv(hass_url, entity_id_hall_tv, api_token):
    url = f"{hass_url}/api/services/light/toggle"
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }
    data = {"entity_id": entity_id_hall_tv}
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        print("Successfully toggled the light")
    else:
        print("Failed to toggle the light")
        
def detect_clap(threshold=0.6):
    def callback(in_data, frame_count, time_info, status):
        ndarray = np.frombuffer(in_data, dtype=np.int16)
        norm = np.linalg.norm(ndarray)
        if norm > threshold * RATE:
            print("Clap detected!")
            return (None, pyaudio.paComplete)
        return (in_data, pyaudio.paContinue)

    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    CHUNK = 1024

    audio = pyaudio.PyAudio()

    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK,
                        stream_callback=callback)

    print("Listening for claps...")
    stream.start_stream()

    return stream, audio

def stop_detect_clap(stream, audio):
    stream.stop_stream()
    stream.close()
    audio.terminate()

def Take_Command():
    r = SR.Recognizer()
    duration = 5  # seconds
    sample_rate = 16000

    print("Jarvis Listening.........")
    audio_data = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype=np.int16)
    sd.wait()

    audio_data = np.squeeze(audio_data)
    audio = SR.AudioData(audio_data.tobytes(), sample_rate, 2)

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

if __name__ == "__main__":
    mac_address = "mac-address"
    stream, audio = detect_clap()
    while True:
        query = Take_Command().lower()
        # Login, Log out, shutdown, restart the system
        if 'wake up daddy\'s home' in query:
            stop_detect_clap(stream, audio)
            toggle_light_led(hass_url, entity_id_led, api_token)
            speak("welcome home sir!")
            while True:
                # Send WoL packet to the computer's network card
                wake_up(mac_address)
                speak("It's good to see you back. Just so you know, I got your back and your data, all your backups have been safely stashed away in the cloud. As always your computer is primed and ready for whatever crazy work schedule you throw at it. Let's show those deadlines who's boss!")
                speak("Would you like me to play your favorite music sir?")
                while True:
                    query = Take_Command().lower()
                    if "yes" in query:
                        speak("Unfortuantely the media source is having issues and needs maintanance, sorry for the trouble sir!")
                        # speak("Sure sir, here you go. Enjoy working!")
                        break
                    else:
                        speak("Ok sir!")
                        break
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
            
        elif 'go to sleep' in query:
            speak("Goodbye Sir! Have a nice day")
            exit()