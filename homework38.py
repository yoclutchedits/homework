import keys
from openai import OpenAI
from huggingface_hub import InferenceClient
import time
from colorama import Fore, init
init(autoreset=True)
def hf(prompt: str, temperature: float = 0.3, max_tokens: int = 512) -> str:
    models = getattr(keys, "HF_MODEL", ["meta-llama/Llama-3.1-8B-Instruct"])
    key = getattr(keys, "hf_key", None)
    if key is None:
        raise ValueError("API key not found. Please set the 'hf_key' variable in the keys module.")
    last_error = None
    for m in models:
        try:
            c = InferenceClient(token=key)
            r = c.chat_completions(
                model=m,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                max_tokens=max_tokens,
            )
            return r.choices[0].message.content
        except Exception as e:
            last_error = e
    return ("hf model failed\n"
            f"models tried: {models}\n"
            "fix\n"
            "1) replace the model list with a single model that works for you\n"
            f"error: {last_error}")
def groq(prompt: str, temperature: float = 0.3, max_tokens: int = 512) -> str:
    GROQ_URL = "https://api.groq.com/openai/v1"
    model = getattr(keys, "GROQ_MODEL", ["llama-3.1-8b-instant", "mixtral-8x7b-32768"])
    key = getattr(keys, "g_key", None)
    if key is None:
        raise ValueError("API key not found. Please set the 'g_key' variable in the keys module.")
    c = OpenAI(api_key=key, base_url=GROQ_URL)
    last_error = None
    for m in model:
        try:
            r = c.chat.completions.create(
                model=m,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                max_tokens=max_tokens
            )
            return r.choices[0].message.content
        except Exception as e:
            last_error = e
            continue
    return ("groq model failed\n"
            f"models tried: {model}\n"
            "fix\n"
            "1) replace the model list with a single model that works for you\n"
            f"error: {last_error}")
def choose_model():
    m = input("Choose a model (hf/groq): ").strip().lower()
    if m == "hf":
        return hf
    elif m == "groq":
        return groq
    else:
        print(Fore.RED + "Invalid choice. Defaulting to groq.")
        return groq
def main():
    print(Fore.MAGENTA + "="*100)
    print(f"{Fore.CYAN}advanced prompting: temperature + instructions")
    print(f"{Fore.MAGENTA}="*100)
    print("part 1: temperature")
    base=input(f"{Fore.YELLOW}enter a prompt: ").strip()
    for t,label in [(0.1, "low"), (0.5, "medium"), (1.0, "high")]:
        print(f"{Fore.CYAN}temperature: {t} ({label})")
        print(groq(base, temperature=t, max_tokens=512))
        time.sleep(1)
    print("\npart 2: instructions")
    topic=input(f"{Fore.YELLOW}enter a topic: ").strip()
    prompts = [
    f"Summarize key facts about {topic} in 3-4 sentences.",
    f"Explain {topic} as if I'm a 10-year-old child.",
    f"Write a pro/con list about {topic}.",
    f"Create a fictional news headline from 2050 about {topic}.",
]
    for i, p in enumerate(prompts, 1):
        print(f"{Fore.CYAN}\nprompt {i}: {p}")
        print(groq(p, temperature=0.7, max_tokens=512))
        time.sleep(1)
    print(f"\n{Fore.MAGENTA}part 3: your turn")
    custom_prompt=input(f"{Fore.YELLOW}enter a custom prompt: ").strip()
    try:
        temp=float(input(f"{Fore.YELLOW}enter a temperature (0.0-1.0): ").strip())
        if not (0.0 <= temp <= 1.0):
            raise ValueError("Temperature must be between 0.0 and 1.0")
    except ValueError:
        print(f"{Fore.RED}Invalid temperature. Using default of 0.7.")
        temp = 0.7
    chosen_model = choose_model()
    if chosen_model == hf:
        print(f"\nresponse for custom prompt with temperature {temp} using Hugging Face:")
        hf_response = hf(custom_prompt, temperature=temp, max_tokens=512)
        print(hf_response)
    else:
        print(f"\nresponse for custom prompt with temperature {temp} using Groq:")
        groq_response = groq(custom_prompt, temperature=temp, max_tokens=512)
        print(groq_response)
    print(f"\n{Fore.MAGENTA}reflection")
    print(f"{Fore.CYAN}1) how did changing the temperature affect the responses?")
    print(f"{Fore.CYAN}2) which of the instructions generated the most interesting response and why?")
    print(f"{Fore.CYAN}3) how would you modify the custom prompt to get a different type of response?")
    print(f"{Fore.MAGENTA}generate content -> rewrite -> create a sequence .")
def pseudo_stream(text, delay=0.05):
    for char in text:
        print(char, end="", flush=True)
        time.sleep(delay)
    print()
def bonus_pseudo_streaming():
    choice = input("\nbonus: streaming-like output? (y/n): ").strip().lower()
    if choice == 'y':
        prompt = input(f"{Fore.YELLOW}enter a prompt for streaming response: ").strip()
        response = groq(prompt, temperature=0.7, max_tokens=512)
        print("\nstreaming response:")
        pseudo_stream(response)
if __name__ == "__main__":
    main()