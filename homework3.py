import re,random
from colorama import Fore, init
init(autoreset=True)
d={
    "beaches":["bali","maldives","phuket","miami","bondi"],
    "mountains":["swiss alps","rocky mountains","himalayas","andes"],
    "cities":["new york","paris","tokyo","london","sydney"]
}
j=[
    "Why don't programmers like nature? Too many bugs!",
    "Why did the computer go to the doctor? Because it had a virus!",
    "Why do travelers always feel warm? Because of all their hot spots!"
]
weather = ["Sunny", "Cloudy", "Rainy", "Stormy", "Windy", "Foggy"]
def normalize_input(text):
    return re.sub(r"/s+"," ",text.strip().lower())
def recommend():
    print("what recommendation you want? (beaches/mountains/cities/)")
    p=input("what is you choice?: ")
    p=normalize_input(p)
    if p in d:
        choice=random.choice(d[p])
        print(Fore.GREEN+"You should visit: "+Fore.YELLOW+choice.title())
    else:
        print(Fore.RED+"Sorry, I don't have recommendations for that category.")
def joke():  
    print("want to hear a joke?")  
    jo=input("yes/no: ")
    jo=normalize_input(jo)
    if jo=="yes":
        joke=random.choice(j)
        print(Fore.GREEN+joke)
    else:
        print(Fore.RED+"No problem! Maybe next time.")
def weather():  
    print("want to know the weather forcast?")
    we=input("yes/no: ")
    we=normalize_input(we)
    if we=="yes":
        weather_forecast=random.choice(weather)
        print(Fore.GREEN+"The weather today is: "+Fore.YELLOW+weather_forecast)
    else:
        print(Fore.RED+"No problem! Maybe next time.")
def help():
    print(Fore.GREEN + "\nI can:")
    print(Fore.GREEN + "- Suggest travel spots (say 'recommendation')")
    print(Fore.GREEN + "- Offer packing tips (say 'packing')")
    print(Fore.GREEN + "- Tell a joke (say 'joke')")
    print(Fore.GREEN + "- Tell the weather forcast (say 'forcast')")
    print(Fore.RED + "Type 'exit' or 'bye' to end.\n")

def chat():
    print( "Hello! I'm TravelBot.")
    name = input( "what is Your name? ")
    print( f"Nice to meet you, {name}!")
    
    help()
    
    while True:
        user = input(Fore.YELLOW + f"{name}: ")
        user = normalize_input(user)
        
        if "recommend" in user :
            recommend()
        elif "packing" in user :
            recommend()
        elif "joke" in user :
           joke()
        elif "help" in user:
            help()
        elif "forcast" in user:
            weather()
        elif "exit" in user or "bye" in user:
            print("TravelBot: Safe travels! Goodbye!")
            break
        else:
            print("TravelBot: Could you rephrase?")
# Run the chatbot
if __name__ == "__main__":
    chat()

