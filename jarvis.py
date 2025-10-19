"""
Jarvis AI Assistant (Male Voice + Direct YouTube Play)
"""

import webbrowser
import datetime
import speech_recognition as sr
from youtube_search import YoutubeSearch
import pyttsx3

# Initialize Text-to-Speech engine (male voice)
engine = pyttsx3.init()
voices = engine.getProperty('voices')
for v in voices:
    if 'male' in v.name.lower() or 'david' in v.name.lower():
        engine.setProperty('voice', v.id)
        break
engine.setProperty('rate', 175)

recognizer = sr.Recognizer()
mic = sr.Microphone()

assistant_name = "Jarvis"
speech_out_lang = 'en'

def speak(text):
    engine.say(text)
    engine.runAndWait()

def greet_user():
    hour = datetime.datetime.now().hour
    if 5 <= hour < 12:
        greet = "Good morning"
    elif 12 <= hour < 17:
        greet = "Good afternoon"
    elif 17 <= hour < 21:
        greet = "Good evening"
    else:
        greet = "Hello"

    if speech_out_lang == 'hi':
        greet_hi = {
            "Good morning": "सुप्रभात",
            "Good afternoon": "नमस्कार",
            "Good evening": "शुभ संध्या",
            "Hello": "नमस्ते"
        }
        speak(greet_hi[greet] + " मैं आपकी कैसे मदद कर सकता हूँ?")
    else:
        speak(f"{greet}, I am {assistant_name}. How can I help you?")

def recognize_speech():
    with mic as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        query = recognizer.recognize_google(audio, language="en-IN")
        print("You said (English):", query)
        return query.lower()
    except:
        try:
            query = recognizer.recognize_google(audio, language="hi-IN")
            print("You said (Hindi):", query)
            return query.lower()
        except:
            return ""

def play_youtube(video_name):
    """Play top YouTube result directly."""
    try:
        results = YoutubeSearch(video_name, max_results=1).to_dict()
        if results:
            url = "https://www.youtube.com" + results[0]['url_suffix']
            webbrowser.open(url)
            return True
        return False
    except:
        return False

def main():
    global speech_out_lang
    greet_user()
    speak("Say 'play' followed by a video name to play it on YouTube.")

    while True:
        query = recognize_speech()
        if not query:
            speak("Please say again.")
            continue

        # Exit
        if any(word in query for word in ["exit", "quit", "stop", "bye", "close"]):
            speak("Goodbye, have a great day!")
            break

        # Switch to Hindi
        if "hindi" in query and ("baat" in query or "bolo" in query):
            speech_out_lang = 'hi'
            speak("ठीक है, अब मैं हिंदी में बात करूँगा।")
            continue

        # Switch to English
        if "english" in query:
            speech_out_lang = 'en'
            speak("Okay, I will talk in English now.")
            continue

        # Direct play on YouTube
        if "play" in query or "चलाओ" in query:
            search_term = query.replace("play", "").replace("चलाओ", "").strip()
            if search_term:
                speak(f"Playing {search_term} on YouTube.")
                success = play_youtube(search_term)
                if not success:
                    speak("Sorry, I couldn’t find that video.")
            else:
                speak("Please tell me what to play.")
            continue

        # Time query
        if "time" in query or "kitne baje" in query:
            now = datetime.datetime.now().strftime("%I:%M %p")
            if speech_out_lang == 'hi':
                speak(f"अभी समय है {now}")
            else:
                speak(f"The time is {now}")
            continue

        # Default response
        if speech_out_lang == 'hi':
            speak(f"मैंने सुना {query}")
        else:
            speak(f"I heard {query}")

if __name__ == "__main__":
    speak("Starting Jarvis assistant.")
    main()
