import base64, requests, os
from keys import hf_key
from colorama import init, Fore, Style
init(autoreset=True)
API_URL = "https://router.huggingface.co/v1/chat/completions"
HEADERS = {"Authorization": f"Bearer {hf_key}", "Content-Type": "application/json"}
MODELS = ["Qwen/Qwen3-VL-8B-Instruct:together", "Qwen/Qwen3-VL-32B-Instruct:together"]
def data_url(b: bytes) -> str:
    return "data:image/jpeg;base64," + base64.b64encode(b).decode("utf-8")
def box(title:str,lines:list[str],icon:str):
    w=max(30,len(title) + 4, *(len(x) for x in lines))
    print(Fore.GREEN + "\n" + "┏" + "━" * (w + 2) + "┓")
    print(Fore.GREEN + f"┃ {icon} {title.ljust(w - 2)} ┃")
    print(Fore.GREEN + "┣" + "━" * (w + 2) + "┫")
    for x in lines: print(Fore.GREEN + f"┃ {x.ljust(w)} ┃")
    print(Fore.GREEN + "┗" + "━" * (w + 2) + "┛\n")
def process_images():
    folder = input(Fore.MAGENTA + "Enter folder path: ").strip()
    if not os.path.isdir(folder):
        print(f"{Fore.RED} Folder not found!"); return
    files = [f for f in os.listdir(folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    with open("summary.txt", "w", encoding="utf-8") as report:
        for filename in files:
            path = os.path.join(folder, filename)
            with open(path, "rb") as f: img = f.read()
            caption = "Failed to get caption"
            for model in MODELS:
                payload = {"model": model,"messages": [{"role": "user", "content": [{"type": "text", "text": "Short caption for this image."},{"type": "image_url", "image_url": {"url": data_url(img)}}]}],"max_tokens": 50}
                r = requests.post(API_URL, headers=HEADERS, json=payload)
                if r.status_code == 200:
                    caption = r.json()["choices"][0]["message"]["content"].strip()
                    break
                else:
                    print(f"{Fore.YELLOW} Model {model} failed: {r.status_code} - {r.text}")
            print(f"{Fore.GREEN} Processed: {filename}")
            report.write(f"{filename}: {caption}\n")
    box("Task Finished", [f"Processed {len(files)} images", "Results saved to summary.txt"])
if __name__ == "__main__":
    process_images()