from keys import hf_key
import requests, base64, os, re, time
from PIL import Image
import time
from colorama import init, Fore, Style
init(autoreset=True)
ROUTER_URL = "https://router.huggingface.co/v1/chat/completions"
HEADERS = {"Authorization": f"Bearer {hf_key}", "Content-Type": "application/json"}
VISION_MODELS = [
    "Qwen/Qwen3-VL-8B-Instruct:together",
    "Qwen/Qwen3-VL-32B-Instruct:together",
    "Qwen/Qwen2.5-VL-7B-Instruct:together",
    "Qwen/Qwen2.5-VL-32B-Instruct:together",
    "Qwen/Qwen2-VL-2B-Instruct:together",
    "Qwen/Qwen2-VL-7B-Instruct:together",
]
TEXT_MODELS = [
    "Qwen/Qwen2.5-7B-Instruct:together",
    "Qwen/Qwen2.5-14B-Instruct:together",
    "Qwen/Qwen2.5-32B-Instruct:together",
    "mistralai/Mistral-7B-Instruct-v0.3:together",
    "mistralai/Mixtral-8x7B-Instruct-v0.1:together",
] 
def query_hf_api(payload: dict):
    try:
        r = requests.post(ROUTER_URL, headers=HEADERS, json=payload, timeout=120)
    except requests.RequestException as e:
        return None, f"Request failed: {e}"
    if r.status_code != 200:
        try:
            j = r.json()
            msg = j.get("error", {}).get("message") or str(j)
        except Exception:
            msg = (r.text or "").strip() or r.reason or "Request failed."
        return None, f"Status {r.status_code}: {msg}"
    try:
        return r.json(), None
    except Exception:
        return None, "Non-JSON response received from the API."
def _data_url(path: str) -> str:
    with open(path, "rb") as f:
        return "data:image/jpeg;base64," + base64.b64encode(f.read()).decode("utf-8")
def extract_text(data) -> str:
    try:
        return data["choices"][0]["message"]["content"].strip()
    except Exception:
        return ""
def _run_models(models,messages,max_tokens=160,temperature=0.3):
    last_err = None
    for model in models:
        data, err = query_hf_api({"model": model, "messages": messages, "max_tokens": max_tokens, "temperature": temperature})
        if err:
            last_err = err
            continue
        out = extract_text(data) 
        if out:
            return out, None
        last_err=f"Unexpected response format from model {model}: {data}"
    return None, last_err
def words(text: str):
    return re.findall(r"\S+", (text or '').strip())
def extract_n_words(text: str, n: int)-> str:
    return ' '.join(words(text)[:n])
def ensure_sentence_end(text: str) -> str:
    t=(text or '').strip()
    if t and t[-1] not in ".!?":
        t += "."
    return t
def get_basic_caption(image_path: str) -> str:
    print(f"{Fore.YELLOW}🖼️ Generating basic caption ...")
    msgs = [{
        "role": "user",
        "content": [
            {"type": "text", "text": "Write one complete sentence describing this image."},
            {"type": "image_url", "image_url": {"url": _data_url(image_path)}},
        ],
    }]
    cap, err = _run_models(VISION_MODELS, msgs, max_tokens=90, temperature=0.2)
    return cap if cap else f"[Error] {err}"
def generate_text(prompt: str,max_new_tokens: int = 220) -> str:
    txt,err=_run_models(TEXT_MODELS, [{"role": "user", "content": prompt}], max_tokens=max_new_tokens, temperature=0.3)
    if not txt:
        raise Exception(err)
    return txt
def generate_exact_sentence(prompt: str, n_words: int, max_new_tokens: int, tries: int = 6) -> str:
    last = ""
    for _ in range(tries):
        last = generate_text(prompt, max_new_tokens=max_new_tokens)
        if len(words(last)) >= n_words:
            return ensure_sentence_end(extract_n_words(last, n_words))
        prompt += f"\n\nTry again. Ensureat least {n_words} words and end with a period."
        time.sleep(0.2)
    return ensure_sentence_end(extract_n_words(last, min(n_words, len(words(last)))))
def print_menu():
    print(f"""{Style.BRIGHT}{Fore.GREEN}
================ Image-to-Text Conversion =================
Select output type:
1. Caption (5 words)
2. Description (30 words)
3. Summary (50 words)
4. Exit
=============================================================
""")
def main():
    image_path = input(Fore.CYAN + "🖼️ Enter image filename (e.g., test.jpg): ").strip()
    if not os.path.isfile(image_path):
        print(f"{Fore.RED}❌ File not found: {image_path}")
        return
    try:
        Image.open(image_path)
    except Exception as e:
        print(f"{Fore.RED}❌ Invalid image file: {image_path}\nReason: {e}")
        return
    basic_caption= get_basic_caption(image_path)
    print(f"{Fore.CYAN}Basic Caption: {basic_caption}\n")
    time.sleep(1)
    while True:
        print_menu()
        choice = input(Fore.CYAN +"Enter your choice (1-4): ").strip()
        if basic_caption.startswith("[Error]") and choice in {"1", "2", "3"}:
            basic_caption = get_basic_caption(image_path)
            print(f"{Fore.CYAN}Basic Caption: {basic_caption}\n")
            time.sleep(2)
        if choice == "1":
            if basic_caption.startswith("[Error]"):
                print(f"{Fore.RED}Cannot generate caption due to previous error: {basic_caption}")
                continue
            caption = extract_n_words(ensure_sentence_end(basic_caption), 5)
            print(f"{Fore.GREEN}Caption (5 words): {caption}\n")
            time.sleep(2)
        elif choice == "2":
            prompt = f"Expand this short caption into a detailed description of exactly 30 words: {basic_caption}"
            description = generate_exact_sentence(prompt, 30, max_new_tokens=150)
            print(f"{Fore.GREEN}Description (30 words): {description}\n")
            time.sleep(2)
        elif choice == "3":
            prompt = f"Write a comprehensive summary of exactly 50 words based on this description: {basic_caption}"
            summary = generate_exact_sentence(prompt, 50, max_new_tokens=200)
            print(f"{Fore.GREEN}Summary (50 words): {summary}\n")
            time.sleep(2)
        elif choice == "4":
            print(f"{Fore.BLUE}Exiting. Goodbye!")
            break
        else:
            print(f"{Fore.RED}Invalid choice. Please enter a number between 1 and 4.\n")
if __name__ == "__main__":
    main()