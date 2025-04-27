import time
import pyttsx3
import speech_recognition as sr
import eel

def speak(text):
    text = str(text)
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    # print(voices)
    engine.setProperty('voice', voices[0].id)
    eel.DisplayMessage(text)
    engine.say(text)
    engine.runAndWait()
    engine.setProperty('rate', 174)
    eel.receiverText(text)

# Expose the Python function to JavaScript

def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("I'm listening...")
        eel.DisplayMessage("I'm listening...")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source, 10, 8)

    try:
        print("Recognizing...")
        eel.DisplayMessage("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
        eel.DisplayMessage(query)
    
        speak(query)
    except Exception as e:
        print(f"Error: {str(e)}\n")
        return None

    return query.lower()





@eel.expose
def takeAllCommands(message=None):
    if message is None:
        query = takecommand()  # If no message is passed, listen for voice input
        if not query:
            return  # Exit if no query is received
        print(query)
        eel.senderText(query)
    else:
        query = message  # If there's a message, use it
        print(f"Message received: {query}")
        eel.senderText(query)
    
    try:
        if query:
            if "open" in query:
                from backend.feature import openCommand
                openCommand(query)
            elif "send message" in query or "call" in query or "video call" in query:
                from backend.feature import findContact, whatsApp
                flag = ""
                Phone, name = findContact(query)
                if Phone != 0:
                    if "send message" in query:
                        flag = 'message'
                        speak("What message to send?")
                        query = takecommand()  # Ask for the message text
                    elif "call" in query:
                        flag = 'call'
                    else:
                        flag = 'video call'
                    whatsApp(Phone, query, flag, name)
            

            elif "give me news" in query or "news" in query:
              from backend.feature import get_latest_news
              get_latest_news()


            if "open" in query:
              from backend.feature import openWebsite, openCommand
              # First, try known websites
              if any(site in query.lower() for site in ["youtube", "instagram", "twitter", "facebook", "google", "linkedin", "github","wikipedia"]):
                  openWebsite(query)
              else:
                  openCommand(query)    
                  
            
            elif "temperature" in query or "weather" in query:
              speak("Which city are you asking about?")
              city = takecommand()
              if city:
                from backend.feature import get_city_temperature
                get_city_temperature(city)



            elif "solve" in query and "program" in query or "programming problem" in query:
              speak("What programming problem would you like me to solve?")
              problem = takecommand()
            if problem:
              from backend.feature import solve_programming_problem
              solution = solve_programming_problem(problem)
              print(solution)


            #elif "on youtube" in query:
                #from backend.feature import PlayYoutube
                #PlayYoutube(query)
            else:
                from backend.feature import chatBot
                chatBot(query)
        else:
            speak("No command was given.")
    except Exception as e:
        print(f"An error occurred: {e}")
        speak("Sorry, something went wrong.")
 
    
    eel.ShowHood()