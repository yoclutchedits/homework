import speech_recognition as sr
import pyttsx3
import webbrowser
import random
import requests
from datetime import datetime
def speak(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    engine.say(text)
    engine.runAndWait()
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
    try:
        command = recognizer.recognize_google(audio)
        print(f"You said: {command}")
        return command.lower()
    except sr.UnknownValueError:
        print("Sorry, I did not understand that.")
        return ""
    except sr.RequestError:
        print("Sorry, my speech service is down.")
        return ""
def tell_joke():
    try:
        joke = requests.get("https://official-joke-api.appspot.com/random_joke").json()
        speak(f"Here's a joke: {joke['setup']} ... {joke['punchline']}")
    except:
        speak("Sorry, I couldn't fetch a joke at the moment.")
def fun_fact():
    try:
        fact = requests.get("https://uselessfacts.jsph.pl/random.json?language=en").json()
        speak(f"Did you know? {fact['text']}")
    except:
        speak("Sorry, I couldn't fetch a fact at the moment.")
def respond_to_command(command):
    if "hello" in command:
        speak("Hello! How can I assist you today?")
    elif "your name" in command or "who are you" in command:
        speak("I am your virtual assistant.")
    elif "time" in command:
        now = datetime.now().strftime("%I:%M %p")
        speak(f"The current time is {now}.")
    elif "google" in command:
        query = command.replace("google", "").strip()
        if not query:
            speak("Opening Google")
            webbrowser.open("https://www.google.com")
        else:
            speak(f"Searching Google for {query}")
            webbrowser.open(f"https://www.google.com/search?q={query}")
    elif "youtube" in command:
        speak("Opening YouTube")
        webbrowser.open(f"https://www.youtube.com/")
    elif "github" in command:
        speak("Opening GitHub")
        webbrowser.open(f"https://www.github.com/")
    elif "instagram" in command:
        speak("Opening Instagram")
        webbrowser.open(f"https://www.instagram.com/")
    elif "twitter" in command:
        speak("Opening Twitter")
        webbrowser.open(f"https://www.twitter.com/")
    elif "facebook" in command:
        speak("Opening Facebook")
        webbrowser.open(f"https://www.facebook.com/")
    elif "linkedin" in command:
        speak("Opening LinkedIn")
        webbrowser.open(f"https://www.linkedin.com/")
    elif "reddit" in command:
        speak("Opening Reddit")
        webbrowser.open(f"https://www.reddit.com/")
    elif "netflix" in command:
        speak("Opening Netflix")
        webbrowser.open(f"https://www.netflix.com/")
    elif "amazon" in command:
        speak("Opening Amazon")
        webbrowser.open(f"https://www.amazon.com/")
    elif "spotify" in command:
        speak("Opening Spotify")
        webbrowser.open(f"https://www.spotify.com/")
    elif "play a song" in command:
        lists=["https://music.youtube.com/watch?v=kJQP7kiw5Fk",
        "https://music.youtube.com/watch?v=9HDEHj2yzew",  
        "https://music.youtube.com/watch?v=4NRXx6U8ABQ",  
        "https://music.youtube.com/watch?v=09R8_2nJtjg", 
        "https://music.youtube.com/watch?v=IcrbM1l_BoI", 
        "https://music.youtube.com/watch?v=V1Pl8CzNzCw", 
        "https://music.youtube.com/watch?v=fHI8X4OXluQ",
        "https://music.youtube.com/watch?v=TuvcZfQe-Kw",
        "https://music.youtube.com/watch?v=7X_WvvK50mY",
        "https://music.youtube.com/watch?v=pAgnJDJN4VA"]
        r=random.choice(lists)
        speak("Playing a random song")
        webbrowser.open(r)
    elif "menu" in command:
        speak("Here are some commands you can try: hello, your name, time, google [search], youtube, github, instagram, spotify, play a song, joke, fact, exit")
    elif "joke" in command:
        tell_joke()
    elif "fact" in command:
        fun_fact()
    elif "exit" in command or "quit" in command:
        speak("Goodbye!")
        return False
    else:
        speak("I'M NOT SURE HOW TO RESPOND TO THAT.")
        speak("Try saying 'menu' to see the list of commands.")
    return True
def main():
    speak("Welcome! I am your virtual assistant. How can I help you?")
    print("Say 'exit' or 'quit' to stop the assistant.")
    print("say 'menu' to see the list of commands.")
    while True:
        command = listen()
        if command:
            if not respond_to_command(command):
                break
if __name__ == "__main__":
    main()