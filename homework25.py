import requests
from keys import hf_key
from PIL import Image
import time
from io import BytesIO
from datetime import datetime
from huggingface_hub import InferenceClient
from colorama import Fore, Style, init
init(autoreset=True)
models="stabilityai/stable-diffusion-xl-base-1.0"
API_URL = f"https://router.huggingface.co/hf-inference/models/{models}"
HEADERS = {"Authorization": f"Bearer {hf_key}", "Accept": "image/png", "Content-Type": "application/json"}
def json(r: requests.Response) -> str:
    try:
        return r.json()
    except Exception as e:
        print(f"{Fore.RED}error parsing json: {e}")
        return {"error": "invalid json response"}
def generate_image_from_text(prompt: str, negative_prompt: str = None) -> Image.Image:
    payloads=[]
    if negative_prompt:
        payloads.append({"inputs": {"prompt": prompt, "negative_prompt": negative_prompt}})
        payloads.append({"inputs": prompt, "parameters": {"negative_prompt": negative_prompt}})
        payloads.append({"inputs": prompt, "options": {"negative_prompt": negative_prompt}})
    payloads.append({"inputs": {"prompt": prompt}})
    payloads.append({"inputs": prompt})
    last_err=None
    for payload in payloads:
        for a in range(3):
            try:
                r = requests.post(API_URL, headers=HEADERS, json=payload, timeout=30)
            except Exception as e:
                last_err=f"request error: {e}"
                break
            ct=(r.headers.get("Content-Type") or "").lower()
            if r.status_code == 200 and ct.startswith("image/"):
                return Image.open(BytesIO(r.content))
            last_err = f"{r.status_code}: {json(r)}"
            if r.status_code in (502, 503, 504):
                time.sleep(1 + a)
                continue
            break
    raise Exception(Fore.RED + last_err or Fore.RED + "The response is not an image. Possibly an error message.")
def main():
    n=None
    print(Fore.MAGENTA + "welcome to the image generation tool!")
    print(Fore.CYAN + "Type 'exit' to quit.\n")
    while True:
        prompt = input(Fore.MAGENTA + "Enter a prompt: ").strip()
        if prompt.lower() in ("exit", "quit"):
            print(Fore.GREEN + "goodbye!")
            break
        if not prompt:
            print(Fore.RED + "please enter a prompt")
            continue
        neg_prompt_input = input(Fore.CYAN + "Enter a negative prompt (or press Enter to skip):\n> ").strip()
        negative_prompt = neg_prompt_input if neg_prompt_input else None
        print(f"{Fore.MAGENTA}generating image for prompt: {prompt}")
        try:
            while True:
                if n=="n":
                    print(Fore.CYAN+"recreating image")
                    image = generate_image_from_text(prompt, negative_prompt)
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"generated_image_{timestamp}.png"
                    image.show()
                    n=input(Fore.MAGENTA+"did the image meet your expetation (y/n)").strip().lower()
                if n==None:
                    image = generate_image_from_text(prompt, negative_prompt)
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"generated_image_{timestamp}.png"
                    image.show()
                    n=input(Fore.MAGENTA+"did the image meet your expetation (y/n)").strip().lower()
                if n!="n":
                    break
            y=input(f"{Fore.CYAN}Save image as {filename}? (y/n): ").strip().lower()
            if y == "y":
                image.save(filename)
                print(f"{Fore.GREEN}image saved as {filename}")
            else:
                print(Fore.MAGENTA + "image not saved")
            print()
        except Exception as e:
            print(f"{Fore.RED}failed to generate image: {e}")
            print(Fore.RED + "please try again later\n")
if __name__ == "__main__":
    main()