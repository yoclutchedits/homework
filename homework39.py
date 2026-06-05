import keys
from openai import OpenAI
from huggingface_hub import InferenceClient
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
            
    return f"HF model failed. Models tried: {models}. Error: {last_error}"
def groq(prompt: str, temperature: float = 0.3, max_tokens: int = 512) -> str:
    GROQ_URL = "https://api.groq.com/openai/v1"
    models = getattr(keys, "GROQ_MODEL", ["llama-3.1-8b-instant", "mixtral-8x7b-32768"])
    key = getattr(keys, "g_key", None)
    if key is None:
        raise ValueError("API key not found. Please set the 'g_key' variable in the keys module.")
    c = OpenAI(api_key=key, base_url=GROQ_URL)
    last_error = None
    for m in models:
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
            
    return f"Groq model failed. Models tried: {models}. Error: {last_error}"
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
    print("=== Zero-shot, One-shot & Few-shot Prompting ===")
    category = input("Enter category (e.g., 'math', 'history', 'science'): ").strip()
    item = input("Enter an item in that category: ").strip()
    if not category or not item:
        print(Fore.RED + "Category and item cannot be empty.")
        return
    c_m = choose_model()
    zero_shot = f"Is '{item}' related to the category '{category}'? Answer with yes or no."
    print(f"\n{Fore.GREEN}--- ZERO-SHOT PROMPTING ---")
    print(c_m(zero_shot, temperature=0.3, max_tokens=1024))
    one_shot = f"""Category: fruit
    Item: apple
    Answer: Yes, apple is a fruit.
    Now you try:
    Category: {category}
    Item: {item}
    Answer:"""
    print(f"\n{Fore.GREEN}--- ONE-SHOT PROMPTING ---")
    print(c_m(one_shot, temperature=0.3, max_tokens=1024))
    few_shot = f"""Category: fruit
    Item: apple
    Answer: Yes, apple is a fruit.
    Category: country
    Item: Nepal
    Answer: Yes, Nepal is a country.
    Category: planet
    Item: Mars
    Answer: Yes, Mars is a planet.
    Now you try:
    Category: {category}
    Item: {item}
    Answer:"""
    print(f"\n{Fore.GREEN}--- FEW-SHOT PROMPTING ---")
    print(c_m(few_shot, temperature=0.3, max_tokens=1024))
    print(f"\n{Fore.GREEN}--- YOUR TURN TO BE CREATIVE ---")
    word = input(f"{Fore.YELLOW}Write the word you want a one-sentence story about: ").strip()
    mode = input(f"{Fore.YELLOW}How many examples do you want to provide? (0 for zero-shot, 1 for one-shot, 2 for few-shot): ").strip()
    base_instruction = "Write a creative one-sentence story about the given word.\n"
    if mode == "1":
        ex_word = input(f"{Fore.YELLOW}Enter your example word: ").strip()
        ex_story = input(f"{Fore.YELLOW}Enter your example story: ").strip()
        creative_prompt = f"{base_instruction}\nExample 1:\nWord: {ex_word}\nStory: {ex_story}\n\nNow you try:\nWord: {word}\nStory:"
    elif mode == "2":
        w1 = input(f"{Fore.YELLOW}First example word: ").strip()
        s1 = input(f"{Fore.YELLOW}First example story: ").strip()
        w2 = input(f"{Fore.YELLOW}Second example word: ").strip()
        s2 = input(f"{Fore.YELLOW}Second example story: ").strip()
        creative_prompt = f"{base_instruction}\nExample 1:\nWord: {w1}\nStory: {s1}\n\nExample 2:\nWord: {w2}\nStory: {s2}\n\nNow you try:\nWord: {word}\nStory:"
    else:
        if mode != "0":
            print(Fore.RED + "Invalid choice. Defaulting to zero-shot.")
        creative_prompt = f"{base_instruction}\nWord: {word}\nStory:"
    print(f"\nResponse: {c_m(creative_prompt, temperature=0.7, max_tokens=1024)}")
    print(f"\n{Fore.CYAN}--- REFLECTION QUESTIONS ---")
    print(f"{Fore.MAGENTA}1. How did the responses differ between zero-shot, one-shot, and few-shot?")
    print(f"{Fore.MAGENTA}2. Which approach gave the most structured/helpful response?")
    print(f"{Fore.MAGENTA}3. How did the tone of your creative examples alter the final story output?")
if __name__ == "__main__":
    main()