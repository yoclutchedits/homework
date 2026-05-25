import speech_recognition as sr
import pyttsx3
from googletrans import Translator
def speak(text, language_code):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    voices = engine.getProperty('voices')
    matched_voice = None
    for voice in voices:
        if language_code in voice.name.lower() or (hasattr(voice, 'languages') and any(language_code in l.lower() for l in voice.languages)):
            matched_voice = voice.id
            break
    if matched_voice:
        engine.setProperty('voice', matched_voice)
    else:
        print(f"Note: Native system voice for '{language_code}' not found. Using default voice.")
    engine.say(text)
    engine.runAndWait()
def translate_text(text, src_language, dest_language):
    translator = Translator()
    try:
        translation = translator.translate(text, src=src_language, dest=dest_language)
        print(f"Translated text: {translation.text}")
        return translation.text
    except Exception as e:
        print(f"Translation error: {e}")
        return text
def speech_to_text(language_code):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
    try:
        command = recognizer.recognize_google(audio, language=language_code)
        print(f"You said: {command}")
        return command
    except sr.UnknownValueError:
        print("Sorry, I did not understand that.")
        return ""
    except sr.RequestError:
        print("Sorry, my speech service is down.")
        return ""
def display_language_options1():
    print("🤖 Available languages to SPEAK in: ")
    print("1. Hindi (hi)")
    print("2. English (en)")
    print("3. Spanish (es)")
    p = input("Enter the number corresponding to your language choice: ")
    language_map = {
        "1": "hi",
        "2": "en",
        "3": "es"
    }
    return language_map.get(p, "en")
def display_language_options2():
    print("🔄 Available translation languages to HEAR: ")
    print("1. Hindi (hi)")
    print("2. Tamil (ta)")
    print("3. Telugu (te)")
    print("4. Bengali (bn)")
    print("5. Marathi (mr)")
    print("6. Gujarati (gu)")
    print("7. Malayalam (ml)")
    print("8. Punjabi (pa)")
    print("9. Spanish (es)")
    print("10. English (en)")
    choice = input("Enter the number corresponding to your language choice: ")
    language_map = {
        "1": "hi",
        "2": "ta",
        "3": "te",
        "4": "bn",
        "5": "mr",
        "6": "gu",
        "7": "ml",
        "8": "pa",
        "9": "es",
        "10": "en"
    }
    return language_map.get(choice, "es")
def main():
    dest_language1 = display_language_options1()
    dest_language2 = display_language_options2()
    original_text = speech_to_text(dest_language1)
    if original_text:
        translated_text = translate_text(original_text, src_language=dest_language1, dest_language=dest_language2)
        print(f"Original text: {original_text}")
        print(f"Translated text: {translated_text}")
        speak(translated_text, language_code=dest_language2)
if __name__ == "__main__":   
    main()