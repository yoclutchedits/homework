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
    m = input(Fore.MAGENTA + "Choose a model (hf/groq): ").strip().lower()
    if m == "hf":
        return hf
    elif m == "groq":
        return groq
    else:
        print(Fore.RED + "Invalid choice. Defaulting to groq.")
        return groq
def bias_mitigation():
    print(f"{Fore.CYAN}welcome to bias mitigation")
    generate_response = choose_model()
    prompt = input(f"{Fore.MAGENTA}enter a prompt to test for bias: ")
    if not prompt:
        print(Fore.RED + "no prompt entered,enter a prompt to test for bias")
        return
    
    i_r=generate_response(prompt, temperature=0.3, max_tokens=1024)
    print(f"{Fore.GREEN}initial response:")
    print(i_r)
    time.sleep(1.5)
    m_prompt = input(f"{Fore.MAGENTA}enter a prompt to make it more nuetral: ")
    if  m_prompt:
        m_r=generate_response(m_prompt, temperature=0.3, max_tokens=1024)
        print(f"{Fore.GREEN}mitigated response:")
        print(m_r)
        time.sleep(1.5)
    else:
        print(Fore.RED + "no prompt entered,skipping mitigation")
        time.sleep(0.5)
def token_limitations_activity():
    print(f"{Fore.CYAN}welcome to token limitations activity")
    time.sleep(0.5)
    generate_response = choose_model()
    prompt = input(f"{Fore.MAGENTA}enter a long prompt: ")
    if prompt:
        l_r=generate_response(prompt, temperature=0.3, max_tokens=1024)
        preview = (l_r[:500] + '...') if len(l_r) > 500 else l_r
        print(f"{Fore.GREEN}response (truncated to 500 characters):")
        print(preview)
        time.sleep(1.5)
    else:
        print(Fore.RED + "no prompt entered,skipping token limitations activity")
        time.sleep(0.5)
    s_prompt = input(f"{Fore.MAGENTA}enter a short prompt: ")
    if s_prompt:
        s_r=generate_response(s_prompt, temperature=0.3, max_tokens=1024)
        print(f"{Fore.GREEN}response:")
        print(s_r)
        time.sleep(1.5)
    else:
        print(Fore.RED + "no prompt entered,skipping short prompt activity")
        time.sleep(0.5)
def main():
    print(f"{Fore.CYAN}welcome to the classwork 41 activities")
    while True:
        print("\nselect an activity:")
        time.sleep(0.5)
        print("1) bias mitigation")
        time.sleep(0.5)
        print("2) token limitations")
        time.sleep(0.5)
        print("3) exit")
        time.sleep(0.5)
        choice = input(f"{Fore.MAGENTA}enter your choice (1/2/3): ")
        if choice == "1":
            bias_mitigation()
        elif choice == "2":
            token_limitations_activity()
        elif choice == "3":
            print(Fore.GREEN + "exiting the activities. goodbye!")
            time.sleep(0.5)
            break
        else:
            print(Fore.RED + "invalid choice, please enter 1, 2, or 3.")
            time.sleep(0.5)
if __name__ == "__main__":
    main()