import requests #warning! i couldn't find the api for spam detection, so the detection may be wrong
from keys import hf_key as k
from colorama import Fore, Style, init
init(autoreset=True)
MODEL = "facebook/bart-large-mnli"
API_URL = f"https://router.huggingface.co/hf-inference/models/{MODEL}"
HEADERS = {"Authorization": f"Bearer {k}"}
TOPICS = ["Spam", "Safe"]
def classify_message(message: str):
    payload = {"inputs": message, "parameters": {"candidate_labels": TOPICS}}
    r= requests.post(API_URL, headers=HEADERS, json=payload, timeout=30)
    if not r.ok:
        raise RuntimeError(f"API error: {r.status_code}")
    return r.json()
def best_topic(prediction: list):
    if not prediction:
        raise ValueError("Empty prediction list")
    best = max(prediction, key=lambda x: x.get("score", 0))
    return best.get("label"), best.get("score")
def bar(score: float) -> str:
    blocks = int(score * 10)
    return "█" * blocks + "░" * (10 - blocks)
def show(message: str, prediction: list):
    top_label, top_score = best_topic(prediction)
    print(Fore.MAGENTA + "\n" + "=" * 60)
    print(Fore.MAGENTA + "Spam vs Safe Message Classifier")
    print(Fore.MAGENTA + "=" * 60)
    print(Fore.CYAN + f"Message: {message}")
    print(Fore.CYAN + f"best topic: {top_label}")
    print(Fore.CYAN + f"Confidence: {round(top_score*100,1)}% [{bar(top_score)}]")
    print(Fore.CYAN + "\nTop guesses:")
    top= sorted(prediction, key=lambda x: x.get("score", 0), reverse=True)
    for i, p in enumerate(top, start=1):
        lbl = p.get("label", "N/A")
        sc = p.get("score", 0)
        print(f"{Fore.CYAN}{i}. {lbl:<12}{round(sc*100,1)}% {bar(sc)}")
    print(Fore.MAGENTA + "=" * 60)
def main():
    print(Fore.MAGENTA + "Welcome to the spam message classifier!")
    print(Fore.MAGENTA + "Enter a message to see if it's likely spam or safe.")
    print(Fore.MAGENTA + "Type 'exit' to quit.")
    while True:
        message = input(Fore.MAGENTA + "\nEnter message: ").strip()
        if message.lower() == "exit":
            print("Goodbye!")
            break
        if not message:
            print(Fore.RED + "Please enter a valid message.")
            continue
        try:
            prediction = classify_message(message)
            if isinstance(prediction, list) and prediction and "label" in prediction[0]:
                show(message, prediction)
            else:
                print(Fore.RED + f"Unexpected response format from API.")
        except Exception as e:
            print(Fore.RED + f"An error occurred: {e}")
if __name__ == "__main__":
    main()