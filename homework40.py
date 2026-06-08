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
    m = input("Choose a model (hf/groq): ").strip().lower()
    if m == "hf":
        return hf
    elif m == "groq":
        return groq
    else:
        print(Fore.RED + "Invalid choice. Defaulting to groq.")
        return groq
def reinforce_learning():
    print("Reinforcement Learning ")
    generate_response = choose_model()
    original_prompt = input("Enter a prompt for the model: ").strip()
    if not original_prompt:
        print("Prompt cannot be empty.")
        return
    i_response = generate_response(original_prompt, temperature=0.3, max_tokens=1024)
    print(Fore.YELLOW + "processing response...")
    time.sleep(1.5)
    print(Fore.CYAN + "initial response:", i_response)
    time.sleep(2)
    try:
        rating = int(input(Fore.MAGENTA + "Rate the response on a scale of 1 to 5: ").strip())
        if rating < 1 or rating > 5:
            print(Fore.RED + "Rating must be between 1 and 5.")
            time.sleep(0.5)
            return
        elif rating >= 4:
            print(Fore.GREEN + "Great! No improvements needed.")
            time.sleep(0.5)
            return
        elif rating <=3:
            while True:
                print(Fore.GREEN + "Thank you for the feedback. Let's work on improving the response.")
                time.sleep(0.5)
                feedback = input(Fore.MAGENTA + "Provide feedback to improve the response: ").strip()
                imp_feedback =(f"Original Task Goal: {original_prompt}\n\n"
                f"Your Previous Attempt: {i_response}\n\n"
                f"Instruction: Revise your previous attempt based strictly on this feedback: {feedback}")
                imp_response = generate_response(imp_feedback, temperature=0.3, max_tokens=1024)
                print(Fore.YELLOW + "processing improved response...")
                time.sleep(1.5)
                print(Fore.CYAN + "Improved response:", imp_response)
                time.sleep(2)
                try:
                    rating = int(input(Fore.MAGENTA + "Rate the improved response on a scale of 1 to 5: ").strip())
                    if rating < 1 or rating > 5:
                        print(Fore.RED + "Rating must be between 1 and 5.")
                        time.sleep(0.5)
                        continue
                    elif rating >= 4:
                        print(Fore.GREEN + "Great! No further improvements needed.")
                        time.sleep(0.5)
                        break
                    else:
                        print(Fore.GREEN + "Thank you for the feedback. Let's continue improving the response.")
                        time.sleep(0.5)
                        i_response = imp_response
                except ValueError:
                    print(Fore.RED + "Invalid rating. Please enter a number between 1 and 5.")
                    time.sleep(0.5)
                    continue
    except ValueError:
        print(Fore.RED + "Invalid rating. Please enter a number between 1 and 5.")
        time.sleep(0.5)
        rating = 3
    print(Fore.YELLOW + "reflection questions:")
    time.sleep(0.5)
    print(Fore.YELLOW + "1) What did you like about the initial response?")
    time.sleep(0.5)
    print(Fore.YELLOW + "2) What did you dislike about the initial response?")
    time.sleep(0.5)
    print(Fore.YELLOW + "3) How did the feedback and rating influence the improved response?")
    time.sleep(0.5)
    print(Fore.YELLOW + "4) What would you do differently next time to get a better response?")
    time.sleep(0.5)
def role_based_prompts():
    print(Fore.GREEN + "Role-based Prompts")
    time.sleep(0.5)
    generate_response = choose_model()
    category = input(Fore.MAGENTA + "Choose a category (e.g., 'science', 'history', 'technology'): ").strip().lower()
    item = input(Fore.MAGENTA + "Enter a specific item within that category (e.g., 'black holes' for science): ").strip().lower()
    if not category or not item:
        print(Fore.RED + "Category and item cannot be empty.")
        time.sleep(0.5)
        return
    teacher_prompt = f"As a teacher, explain the concept of {item} in the context of {category} to a student."
    expert_prompt = f"As an expert in {category}, provide a detailed analysis of {item}."
    teacher_response = generate_response(teacher_prompt, temperature=0.3, max_tokens=1024)
    expert_response = generate_response(expert_prompt, temperature=0.3, max_tokens=1024)
    print(Fore.GREEN + "Teacher's Response:")
    print(Fore.CYAN + teacher_response)
    time.sleep(2)
    print(Fore.GREEN + "Expert's Response:")
    print(Fore.CYAN + expert_response)
    time.sleep(2)
    print(Fore.YELLOW + "reflection questions:")
    print(Fore.YELLOW + "1) How does the teacher's explanation differ from the expert's analysis?")
    time.sleep(0.5)
    print(Fore.YELLOW + "2) What unique insights does each perspective provide?")
    time.sleep(0.5)
    print(Fore.YELLOW + "3) Which response is more helpful for a student's understanding?")
    time.sleep(0.5)
    print(Fore.YELLOW + "4) How can the responses be combined to create a more comprehensive explanation?")
    time.sleep(0.5)
def main():
    print(Fore.GREEN + "Welcome to the AI Learning and Role-based Prompting Exercise!")
    time.sleep(0.5)
    print(Fore.GREEN + "Choose an exercise:")
    time.sleep(0.5)
    print(Fore.CYAN + "1) Reinforcement Learning")
    time.sleep(0.5)
    print(Fore.CYAN + "2) Role-based Prompts")
    time.sleep(0.5)
    choice = input(Fore.MAGENTA + "Enter the number of your choice: ").strip()
    if choice == '1':
        reinforce_learning()
    elif choice == '2':
        role_based_prompts()
    else:
        print(Fore.RED + "Invalid choice. Please enter 1 or 2.")
if __name__ == "__main__":
    main()