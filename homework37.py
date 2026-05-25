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
            # FIX: Added model=m so it actually uses the loop's model
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
    model_func = choose_model()
    print(Fore.CYAN + f"welcome to the prompt engineering class")
    vauge_prompt = input(Fore.MAGENTA + "enter a vauge prompt: ")
    print(Fore.YELLOW + f"generating response...")
    response = model_func(vauge_prompt)
    print(Fore.GREEN + f"="*100)
    print(Fore.GREEN + f"response: {response}")
    print(Fore.GREEN + f"="*100)
    time.sleep(1)
    specific_prompt = input(Fore.MAGENTA + "enter a more specific prompt: ")
    print(Fore.YELLOW + f"generating response...")
    response = model_func(specific_prompt)
    print(Fore.GREEN + f"="*100)
    print(Fore.GREEN + f"response: {response}")
    print(Fore.GREEN + f"="*100)
    time.sleep(1)
    context_prompt = input(Fore.MAGENTA + "enter a prompt with more context: ")
    print(Fore.YELLOW + f"generating response...")
    response = model_func(context_prompt)
    print(Fore.GREEN + f"="*100)
    print(Fore.GREEN + f"response: {response}")
    print(Fore.GREEN + f"="*100)
    time.sleep(1)
    print(Fore.CYAN + f"reflect on the differences in the responses and how the prompt affected the output")
    print(Fore.YELLOW + "1) how did the responses differ?")
    print(Fore.YELLOW + "2) how did the prompt affect the output?")
    print(Fore.YELLOW + "3) which prompt produced the best response and why?")
if __name__ == "__main__":
    main()