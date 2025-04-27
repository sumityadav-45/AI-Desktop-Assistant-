
from compileall import compile_path
import os
import re
from shlex import quote
import struct
import subprocess
import time
import webbrowser
import eel
from hugchat import hugchat 
import pvporcupine
import pyaudio
import pyautogui
import pywhatkit as kit
import pygame
import requests
from backend.command import speak
from backend.config import ASSISTANT_NAME
from hugchat import hugchat
import sqlite3


from backend.helper import extract_yt_term, remove_words
conn = sqlite3.connect("jarvis.db")
cursor = conn.cursor()
# Initialize pygame mixer
pygame.mixer.init()

# Define the function to play sound
@eel.expose
def play_assistant_sound():
    sound_file = r"frontend\\assets\\vendore\\texllate\\audio\\audio_start_sound.mp3"
    pygame.mixer.music.load(sound_file)
    pygame.mixer.music.play()
    
    
def openCommand(query):
    query = query.replace(ASSISTANT_NAME,"")
    query = query.replace("open","")
    query.lower()
    
    app_name = query.strip()

    if app_name != "":

        try:
            cursor.execute( 
                'SELECT path FROM sys_command WHERE name IN (?)', (app_name,))
            results = cursor.fetchall()

            if len(results) != 0:
                speak("Opening "+query)
                os.startfile(results[0][0])

            elif len(results) == 0: 
                cursor.execute(
                'SELECT url FROM web_command WHERE name IN (?)', (app_name,))
                results = cursor.fetchall()
                
                if len(results) != 0:
                    speak("Opening "+query)
                    webbrowser.open(results[0][0])

                else:
                    speak("Opening "+query)
                    try:
                        os.system('start '+query)
                    except:
                        speak("not found")
        except:
            speak("some thing went wrong")

def openWebsite(query):
    websites = {
        "youtube": "https://www.youtube.com",
        "instagram": "https://www.instagram.com",
        "twitter": "https://www.twitter.com",
        "facebook": "https://www.facebook.com",
        "google": "https://www.google.com",
        "linkedin": "https://www.linkedin.com",
        "github": "https://www.github.com",
        "wikipedia":"https://www.wikipedia.org/"
        
    }

    query = query.lower()
    for name in websites:
        if name in query:
            speak(f"Opening {name}")
            webbrowser.open(websites[name])
            return

    speak("Sorry, I couldn't find that website.")




def get_latest_news():
    speak("Fetching the latest news for you.")

    # Replace with your NewsAPI key or use a sample RSS
    url ="https://newsapi.org/v2/everything?q=tesla&from=2025-03-10&sortBy=publishedAt&apiKey=API_KEY"
                          

    try:
        response = requests.get(url)
        data = response.json()

        articles = data.get("articles", [])
        top_headlines = []

        for i, article in enumerate(articles[:5], 1):
            headline = article["title"]
            top_headlines.append(headline)
            print(f"{i}. {headline}")

        if top_headlines:
            for headline in top_headlines:
                speak(headline)
        else:
            speak("Sorry, I couldn't find any news right now.")

    except Exception as e:
        print(f"Error: {e}")
        speak("There was a problem fetching the news.")



def get_city_temperature(city=""):
    if not city:
        city = "your city"

    speak(f"Getting weather info for {city}")
    try:
        url = f"https://wttr.in/{city}?format=%C+%t"
        response = requests.get(url)
        if response.status_code == 200:
            weather = response.text.strip()
            print(f"Weather in {city}: {weather}")
            speak(f"The weather in {city} is {weather}")
        else:
            speak("Sorry, I couldn't get the weather information.")
    except Exception as e:
        print("Error fetching weather:", e)
        speak("There was an error getting the weather.")


def solve_programming_problem(problem):
    
    chatbot = hugchat.ChatBot(cookie_path="backend\\cookie.json")
    id = chatbot.new_conversation()
    chatbot.change_conversation(id)

    prompt = f"Solve the following programming problem in a simple and clear way:\n{problem}\nPlease include code and explanation."

    try:
        response = chatbot.chat(prompt)
        print("Solution:\n", response)
        speak("Here's what I found. Check your screen for the full code.")
        return response
    except Exception as e:
        print("Error:", e)
        speak("Sorry, I couldn’t solve that right now.")
        return "Error solving the problem."



def hotword():
    porcupine=None
    paud=None
    audio_stream=None
    try:
       
        # pre trained keywords    
        porcupine=pvporcupine.create(keywords=["jarvis","alexa"]) 
        paud=pyaudio.PyAudio()
        audio_stream=paud.open(rate=porcupine.sample_rate,channels=1,format=pyaudio.paInt16,input=True,frames_per_buffer=porcupine.frame_length)
        
        # loop for streaming
        while True:
            keyword=audio_stream.read(porcupine.frame_length)
            keyword=struct.unpack_from("h"*porcupine.frame_length,keyword)

            # processing keyword comes from mic 
            keyword_index=porcupine.process(keyword)

            # checking first keyword detetcted for not
            if keyword_index>=0:
                print("hotword detected")

                # pressing shorcut key win+j
                import pyautogui as autogui
                autogui.keyDown("win")
                autogui.press("j")
                time.sleep(2)
                autogui.keyUp("win")
                
    except:
        if porcupine is not None:
            porcupine.delete()
        if audio_stream is not None:
            audio_stream.close()
        if paud is not None:
            paud.terminate()


def findContact(query):
    
    words_to_remove = [ASSISTANT_NAME, 'make', 'a', 'to', 'phone', 'call', 'send', 'message', 'wahtsapp', 'video']
    query = remove_words(query, words_to_remove)

    try:
        query = query.strip().lower()
        cursor.execute("SELECT Phone FROM contacts WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?", ('%' + query + '%', query + '%'))
        results = cursor.fetchall()
        print(results[0][0])
        mobile_number_str = str(results[0][0])

        if not mobile_number_str.startswith('+91'):
            mobile_number_str = '+91' + mobile_number_str

        return mobile_number_str, query
    except:
        speak('not exist in contacts')
        return 0, 0
    
    
def whatsApp(Phone, message, flag, name):
    

    if flag == 'message':
        target_tab = 12
        jarvis_message = "message send successfully to "+name

    elif flag == 'call':
        target_tab = 7
        message = ''
        jarvis_message = "calling to "+name

    else:
        target_tab = 6
        message = ''
        jarvis_message = "staring video call with "+name


    # Encode the message for URL
    encoded_message = quote(message)
    print(encoded_message)
    # Construct the URL
    whatsapp_url = f"whatsapp://send?phone={Phone}&text={encoded_message}"

    # Construct the full command
    full_command = f'start "" "{whatsapp_url}"'

    # Open WhatsApp with the constructed URL using cmd.exe
    subprocess.run(full_command, shell=True)
    time.sleep(5)
    subprocess.run(full_command, shell=True)
    
    pyautogui.hotkey('ctrl', 'f')

    for i in range(1, target_tab):
        pyautogui.hotkey('tab')

    pyautogui.hotkey('enter')
    speak(jarvis_message)


def chatBot(query):
    user_input = query.lower()
    chatbot = hugchat.ChatBot(cookie_path="backend\\cookie.json")
    id = chatbot.new_conversation()
    chatbot.change_conversation(id)
    response =  chatbot.chat(user_input)
    print(response)
    speak(response)
    return response