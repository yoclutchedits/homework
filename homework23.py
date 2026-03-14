import requests
from keys import hf_key
from colorama import init, Fore, Style
init(autoreset=True)
MODEL_ID = "cardiffnlp/twitter-roberta-base-sentiment-latest"
API_URL = f"https://router.huggingface.co/hf-inference/models/{MODEL_ID}"
HEADERS = {"Authorization": f"Bearer {hf_key}"}
TEXTS = [
    "I love this new phone!",
    "The movie was okay, nothing special.",
    "This product is terrible and I hate it.",
    "The weather is nice today.",
    "I am very disappointed with this service."
]
def bar(score):
    return "█" * int(score * 10) + "░" * (10 - int(score * 10))
def label_emoji(label):
    label = label.lower()
    if "positive" in label:
        return f"{Fore.GREEN} Positive"
    elif "negative" in label:
        return f"{Fore.RED} Negative"
    else:
        return f"{Fore.YELLOW} Neutral"
def show_result(label, score):
    percent = round(score * 100, 1)
    print(f"{Fore.WHITE} Sentiment: {label_emoji(label)}")
    print(f"{Fore.WHITE} Confidence: {percent}% [{bar(score)}]\n")
def analyze_sentiment(text: str):
    payload = {"inputs": text}
    response = requests.post(API_URL,headers=HEADERS,json=payload,timeout=30)
    if not response.ok:
        raise RuntimeError(f"{Fore.RED}API error {response.status_code}: {response.text}")
    result = response.json()
    if isinstance(result, dict) and "error" in result:
        raise RuntimeError(f"{Fore.RED}Error: {result['error']}")
    best = max(result[0], key=lambda x: x["score"])
    return best["label"], best["score"]
def demo():
    print(f"{Fore.MAGENTA}\nDemo Sentiment Analysis\n")
    for i, text in enumerate(TEXTS, start=1):
        label, score = analyze_sentiment(text)
        print(f"{Fore.MAGENTA}{i}) Text: {text}")
        show_result(label, score)
def custom():
    text = input(f"{Fore.CYAN}\nEnter text: ").strip()
    if not text:
        print(f"{Fore.RED}Please enter some text.\n")
        return
    label, score = analyze_sentiment(text)
    show_result(label, score)
def main():
    print(f"{Fore.MAGENTA}\nSentiment Analysis Tool\n")
    while True:
        print(f"{Fore.MAGENTA}Options: demo(d) / custom(c) / exit(q)")
        mode = input(f"{Fore.CYAN}Mode: ").strip().lower()
        if mode in ["exit", "q"]:
            print(f"{Fore.GREEN}Bye! ")
            break
        elif mode in ["demo", "d"]:
            demo()
        elif mode in ["custom", "c"]:
            custom()
        else:
            print(f"{Fore.RED}Invalid option.\n")
if __name__ == "__main__":
    main()