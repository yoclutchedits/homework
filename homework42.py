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
def get_essay_details():
    print("Welcome")
    topic = input(Fore.CYAN + "Enter a topic you want an essay for: ").strip()
    essay_type = input(Fore.CYAN +"What type of essay are you writing: ").strip()
    lengths = ['100 words','200 words' ,'300 words', '900 words', '1200 words', '2000 words']
    print(Fore.MAGENTA +"Select essay word count:")
    for i, l in enumerate(lengths, 1): 
        print(f"{Fore.MAGENTA}{i}) {l}")
    try:
        lex = int(input(Fore.CYAN + "> ").strip())
        length = lengths[lex - 1] if 1 <= lex <= len(lengths) else "300 words"
    except ValueError:
        length = '300 words'
    target_audience = input(Fore.CYAN + "Target audience: ").strip()
    return {"topic": topic, "essay_type": essay_type, "length": length, "target_audience": target_audience}
def generate_essay_response(details):
    generate_response = choose_model()
    try:
        temp = float(input(Fore.CYAN + "Enter temperature (0.1 structured, 0.7 creative): ").strip())
        if not (0.0 <= temp <= 1.0): 
            raise ValueError
    except ValueError:
        print(Fore.RED + "Invalid temp, using 0.3")
        temp = 0.3
    intro_p = f"Write an introduction for a {details['essay_type']} essay about {details['topic']} with a total length target of {details['length']}."
    intro_o = generate_response(intro_p, temperature=temp, max_tokens=1024)
    print("\n--- Generated Introduction ---")
    print(intro_o)
    time.sleep(2)
    print(f"{Fore.MAGENTA}\nWould you like the body written as a full draft or step by step?")
    print(Fore.MAGENTA +"1) Full draft\n2) Step by step")
    choice = input(Fore.CYAN + "> ").strip()
    if choice == "1":
        body_o = f"Write the body paragraphs for a {details['essay_type']} essay about {details['topic']} keeping in mind the target audience: {details['target_audience']}."
        body_o = generate_response(body_o, temperature=temp, max_tokens=1024)
        print("\n--- Full Body Draft ---")
        print(body_o)
        time.sleep(2)
    else:
        body_p = f"Write an outline or step-by-step points for the body of a {details['essay_type']} essay about {details['topic']} for an audience of {details['target_audience']}."
        print(f"{Fore.MAGENTA}\n--- Step by Step Body Outline ---")
        body_s_o = generate_response(body_p, temperature=temp, max_tokens=1024)
        print(body_s_o)
        time.sleep(2)
    print(f"{Fore.MAGENTA}\nGenerating conclusion...")
    conclusion_p = f"Write a conclusion for a {details['essay_type']} essay about {details['topic']} tailored for {details['target_audience']}."
    conclusion_o = generate_response(conclusion_p, temperature=temp, max_tokens=1024)
    print(f"{Fore.MAGENTA}\n--- Generated Conclusion ---")
    print(conclusion_o)
    time.sleep(2)
    try:
        rating = int(input(f"{Fore.CYAN}\nRate satisfaction (1-5): ").strip())
        if rating < 1 or rating > 5: 
            raise ValueError
    except ValueError:
        print(Fore.RED + "Invalid rating, using 3")
        rating = 3
    if rating <= 4:
        user_feedback = input(f"{Fore.CYAN}\nPlease provide feedback to improve the essay: ").strip()
        print(f"{Fore.MAGENTA}\nImproving the essay with feedback: {user_feedback}")
        print(f"{Fore.MAGENTA}\n---- improved essay based on feedback (simulated) ----")
        print(f"{Fore.MAGENTA}\n---introduction---")
        intro_improved = f"Write an introduction for a {details['essay_type']} essay about {details['topic']} with a total length target of {details['length']}.your oringanl intro was: {intro_o}, the feedback was: {user_feedback}"
        improved_intro = generate_response(intro_improved, temperature=temp, max_tokens=1024)
        print(improved_intro)
        time.sleep(2)
        print(f"{Fore.MAGENTA}\n---body---")
        if choice == "1":
            body_improved = f"Write the body paragraphs for a {details['essay_type']} essay about {details['topic']} keeping in mind the target audience: {details['target_audience']}. Your original body was: {body_o}, the feedback was: {user_feedback}"
            improved_body = generate_response(body_improved, temperature=temp, max_tokens=1024)
            print(improved_body)
            time.sleep(2)
        else:
            body_s_improved = f"Write an outline or step-by-step points for the body of a {details['essay_type']} essay about {details['topic']} for an audience of {details['target_audience']}. Your original body outline was: {body_s_o}, the feedback was: {user_feedback}"
            improved_body_s = generate_response(body_s_improved, temperature=temp, max_tokens=1024)
            print(improved_body_s)
            time.sleep(2)
        print(f"{Fore.MAGENTA}\n---conclusion---")
        conclusion_improved = f"Write a conclusion for a {details['essay_type']} essay about {details['topic']} tailored for {details['target_audience']}. Your original conclusion was: {conclusion_o}, the feedback was: {user_feedback}"
        improved_conclusion = generate_response(conclusion_improved, temperature=temp, max_tokens=1024)
        print(improved_conclusion)
        time.sleep(2)
    else:
        print(f"{Fore.MAGENTA}Thank you! The essay looks good.")
def run():
    print(f"{Fore.MAGENTA}Welcome to the Essay Generator CLI")
    details = get_essay_details()
    if not details['topic'] or not details['essay_type']:
        print(f"{Fore.RED}Please provide at least a topic and an essay type to continue.")
        return
    generate_essay_response(details)
if __name__ == "__main__":
    run()