import asyncio
import pyttsx3
import random
import time
import requests
from colorama import init, Fore, Style
import speech_recognition as sr
from googletrans import Translator
init(autoreset=True)
engine = pyttsx3.init()
engine.setProperty("rate", 150)
engine.setProperty("volume", 1.0)
def speak(text, language='en'):
    if language != 'en':
        print(f"{Fore.YELLOW}TTS may not sound correct for {language}. Text: {text}")
        return
    try:
        current_rate = engine.getProperty("rate")
        current_vol = engine.getProperty("volume")
        engine.setProperty("rate", current_rate)
        engine.setProperty("volume", current_vol)
        engine.say(text)
        engine.runAndWait()
        engine.stop()
    except Exception as e:
        print(f"TTS Error: {e}")
def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print(f"{Fore.YELLOW}Listening...{Style.RESET_ALL}")
        try:
            audio = recognizer.listen(source, timeout=5)
            text = recognizer.recognize_google(audio)
            print(f"{Fore.CYAN}You said: {text}{Style.RESET_ALL}")
            return text
        except Exception:
            print(f"{Fore.RED}Could not understand or service is down.{Style.RESET_ALL}")
            return ""
async def translate_text(text, target_language="hi"):
    translator = Translator()
    translation = await asyncio.to_thread(translator.translate, text, dest=target_language)
    return translation.text
def menu():
    print(f"\n{Fore.MAGENTA}{'='*30}")
    print(f"{Fore.MAGENTA}Welcome to the Translation and TTS App")
    print(f"{Fore.CYAN}1. Translate and Speak")
    print(f"{Fore.CYAN}2. Tell me a joke")
    print(f"{Fore.MAGENTA}3. useless fact")
    print(f"{Fore.MAGENTA}4. Sample text to speech")
    print(f"{Fore.CYAN}5. Type something for me to speak")
    print(f"{Fore.MAGENTA}6. Rate and volume control")
    print(f"{Fore.CYAN}7. Exit")
    print(f"{Fore.MAGENTA}{'='*30}")
def tell_joke():
    url = "https://official-joke-api.appspot.com/random_joke"
    res=requests.get(url)
    try:
        if res.status_code==200:
            jd=res.json()
            joke =  f"{jd['setup']}-{jd['punchline']}"
    except Exception as e:
        return f'{Fore.RED}Error: {e}'
    print(f"{Fore.GREEN}{joke}")
    speak(joke)
def sample_tts():
    text = "Hello! This is a sample text to speech conversion."
    print(f"{Fore.MAGENTA}{text}")
    speak(text)
def display_language_options():
    print(f"{Fore.CYAN}Select a language to translate to:")
    print("1. Hindi, 2. Tamil, 3. Telugu, 4. Bengali, 5. Marathi, 6. Gujarati, 7. Malayalam, 8. Punjabi, 9. English")
    choice = input(f"{Fore.CYAN}Choice: {Style.RESET_ALL}").strip()
    language_dict = {"1":"hi", "2":"ta", "3":"te", "4":"bn", "5":"mr", "6":"gu", "7":"ml", "8":"pa"}
    return language_dict.get(choice, "en")
def rate_volume_control_menu():
    print(f"\n{Fore.MAGENTA}{'='*30}")
    print(f"{Fore.CYAN}Rate and Volume Control")
    print("1. Increase Rate / 2. Decrease Rate")
    print("3. Increase Volume / 4. Decrease Volume")
    print("5. Return to Main Menu")
    print(f"{Fore.MAGENTA}{'='*30}")
def get_random_fact():
    url = "https://uselessfacts.jsph.pl/random.json?language=en"
    response = requests.get(url)
    if response.status_code == 200:
        fact_data = response.json()
        print(f"Random Fact: {fact_data['text']}")
    else:
        print("Failed to retrieve a random fact.")
def main():
    while True:
        menu()
        time.sleep(0.5)
        f = input(f"{Fore.CYAN}Enter your choice: {Style.RESET_ALL}").strip()
        if f == "1":
            target_language = display_language_options()
            original_text = speech_to_text()
            if original_text:
                translated_text = asyncio.run(translate_text(original_text, target_language))
                print(f"Translated Text: {translated_text}")
                speak(translated_text, target_language)
        elif f == "2":
            tell_joke()
        elif f == "3":
            get_random_fact()
        elif f == "4":
            sample_tts()
        elif f == "5":
            user_text = input(f"{Fore.CYAN}Type something for me to speak: {Style.RESET_ALL}")
            speak(user_text)
        elif f == "6":
            while True:
                rate_volume_control_menu()
                time.sleep(0.5)
                Y = input(f"{Fore.CYAN}Enter your choice: {Style.RESET_ALL}").strip()
                if Y == "1":
                    rate = engine.getProperty("rate") + 50
                    engine.setProperty("rate", rate)
                    print(f"Rate: {rate}")
                elif Y == "2":
                    rate = engine.getProperty("rate") - 50
                    if rate < 0:
                        print(f"{Fore.RED}Rate cannot be negative. Setting to 0.{Style.RESET_ALL}")
                        rate = 0
                    engine.setProperty("rate", rate)
                    print(f"Rate: {rate}")
                elif Y == "3":
                    vol = min(engine.getProperty("volume") + 0.1, 1.0)
                    engine.setProperty("volume", vol)
                    print(f"Volume: {vol:.1f}")
                elif Y == "4":
                    vol = max(engine.getProperty("volume") - 0.1, 0.0)
                    if vol < 0:
                        print(f"{Fore.RED}Volume cannot be negative. Setting to 0.{Style.RESET_ALL}")
                        vol = 0
                    engine.setProperty("volume", vol)
                    print(f"Volume: {vol:.1f}")
                elif Y == "5":
                    break
        elif f == "7":
            print(f"{Fore.GREEN}Exiting the application. Goodbye!")
            break
        else:
            print(f"{Fore.RED}Invalid choice.")
if __name__ == "__main__":
    main()
    # note the speak function might only work 1 time so to get it work just restart the program and try again. I have tried to fix it but it seems to be a pyttsx3 issue.