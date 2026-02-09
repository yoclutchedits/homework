import requests
from colorama import Fore, Style, init
init(autoreset=True)
OPENWEATHER_API_KEY = "20eccdc6b71a6d2ce51647e2d8bc1e3a"
def get_weather(city="london"):
    url = "http://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": OPENWEATHER_API_KEY, "units": "metric"}
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()
    weather_desc = data["weather"][0]["description"]
    temp = data["main"]["temp"]
    feels_like = data["main"]["feels_like"]
    return f"Weather in {city.title()}: {weather_desc}, {temp}°C (feels like {feels_like}°C)"
def get_cat_fact():
    url = "https://catfact.ninja/fact"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    data = response.json()
    return f"Cat Fact: {data['fact']}"
def get_random_joke():
    url = "https://official-joke-api.appspot.com/random_joke"
    res = requests.get(url, timeout=10)
    if res.status_code == 200:
        jd = res.json()
        return f"{jd['setup']} - {jd['punchline']}"
    else:
        return "Failed to retrieve joke"
def main():
    print(Fore.CYAN + "Welcome user!")
    while True:
        u = input(Fore.YELLOW+ "\nChoose: london weather / cat fact / jokes / exit (l,c,j,e): ").lower()
        if u == "exit":
            print(Fore.GREEN + "Goodbye!")
            break
        while u not in ["london weather", "cat fact", "jokes", "l", "c", "j", "e", "exit"]:
            print(Fore.RED + "Please input: london weather OR cat fact OR jokes")
            u = input(Fore.YELLOW+ "Choose: london weather / cat fact / jokes / exit (l,c,j,e): ").lower()
        if u == "l":
            u = "london weather"
        elif u == "c":
            u = "cat fact"
        elif u == "j":
            u = "jokes"
        elif u == "e":
            u='exit'
        if u == "london weather":
            print(Fore.GREEN + get_weather())
        elif u == "cat fact":
            print(Fore.MAGENTA + get_cat_fact())
        elif u == "jokes":
            print(Fore.BLUE + get_random_joke())
        elif u =='exit':
            print(Fore.RED + "Goodbye!")
            break
if __name__ == "__main__":
    main()
