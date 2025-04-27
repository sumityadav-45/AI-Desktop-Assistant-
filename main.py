import os
import eel
from backend.auth import recoganize
from backend.auth.recoganize import AuthenticateFace
from backend.feature import *
from backend.command import *

def start():
    eel.init("frontend") 
    play_assistant_sound()

    @eel.expose
    def init():
        eel.hideLoader()
        speak(" hello,Welcome sir, How can I help you")
        speak("Ready for Face Authentication")
        flag = recoganize.AuthenticateFace()
        if flag == 1:
            speak("Face recognized successfully")
            eel.hideFaceAuth()
            eel.hideFaceAuthSuccess()
            speak(" hello,Welcome sir, How can I help you")
            eel.hideStart()
            play_assistant_sound()
        else:
            speak("Face not recognized. Please try again")

    os.system('start msedge.exe --app="http://127.0.0.1:8000/index.html"')
    eel.start("index.html", mode=None, host="localhost", block=True)

# ✅ This ensures the script doesn't auto-run when imported in subprocesses
if __name__ == '__main__':
    start()
