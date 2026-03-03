import requests
import random
from colorama import Fore, Style,init
init(autoreset=True)
def get_fact(u, url):
    try:
        res = requests.get(url, timeout=5)
        if res.status_code == 200:
            fact = res.json()
            if u == "1":
                print(f"{Fore.CYAN}Random Fact: {fact['text']}")
            elif u == "2":
                print(f"{Fore.CYAN}Cat Fact: {fact['fact']}")
            elif u == "3":
                url = "https://history.muffinlabs.com/date"
                res = requests.get(url).json()
                event = random.choice(res['data']['Events'])
                print(f"{Fore.CYAN}History: In {event['year']}, {event['text']}")
            elif u == "4":
                print(f"{Fore.CYAN}{fact['setup']}-{fact['punchline']}")
            elif u == "5":
                print(f"{Fore.CYAN}Country Info: {fact[0]['name']['common']}")
                print(f"{Fore.CYAN}Capital: {fact[0]['capital'][0]}")
                print(f"{Fore.CYAN}Population: {fact[0]['population']}")
                print(f"{Fore.CYAN}Area: {fact[0]['area']} km²")
            elif u == "6":
                print(f"{Fore.CYAN}Space Fact: {fact['title']}")
                print(f"{Fore.CYAN}Detail: {fact['explanation'][:250]}...")
    except Exception as e:
        print(f"{Fore.RED}fError: {e}")
print(f"{Fore.GREEN}Welcome to the Fact Generator!")
while True:
    print(f"{Fore.MAGENTA}1. Random | 2. Cats | 3. History | 4. Jokes | 5. Country Info | 6. Space | q. Quit")
    u = input(f"{Fore.MAGENTA}Selection (1-6/q): ").strip().lower()
    if u == "1":
        url = "https://uselessfacts.jsph.pl/random.json?language=en"
        get_fact(u, url)
    elif u == "2":
        url = "https://catfact.ninja/fact"
        get_fact(u, url)
    elif u == "3":
        url = "https://history.muffinlabs.com/date"
        get_fact(u, url)
    elif u == "4":
        url = "https://official-joke-api.appspot.com/random_joke"
        get_fact(u, url)
    elif u == "5":
        c = input("Enter a country name: ")
        url = f"https://restcountries.com/v3.1/name/{c}"
        get_fact(u, url)
    elif u == "6":
        url = "https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY"
        get_fact(u, url)
    elif u == "q":
        print("Closing program...")
        break
    else:
        print("Invalid choice, please try again.")