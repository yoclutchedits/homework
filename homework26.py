import requests
from keys import hf_key
from PIL import Image , ImageEnhance, ImageFilter
import time
from io import BytesIO
from datetime import datetime
from huggingface_hub import InferenceClient
from colorama import Fore, Style, init
init(autoreset=True)
MODELS = [
    "ByteDance/SDXL-Lightning",
    "black-forest-labs/FLUX.1-dev",
    "stabilityai/stable-diffusion-xl-base-1.0",
]
HEADERS = {"Authorization": f"Bearer {hf_key}", "Accept": "image/png"}
def generate_image_from_text(prompt):
    payload, last_err = {"inputs": prompt}, None
    for model in MODELS:
        url = f"https://router.huggingface.co/hf-inference/models/{model}"
        for _ in range(3):
            r = requests.post(url, headers=HEADERS, json=payload, timeout=120)
            ct = (r.headers.get("content-type") or "").lower()
            if r.status_code == 503 and "application/json" in ct:
                try:
                    wait_s = int(r.json().get("estimated_time", 5))
                except Exception:
                    wait_s = 5
                time.sleep(wait_s + 1)
                continue
            if r.status_code == 200 and "application/json" not in ct:
                try:
                    return Image.open(BytesIO(r.content)).convert("RGB")
                except Exception as e:
                    last_err = f"Request failed with status code 200: Could not decode image bytes: {e}"
                    break
            try:
                body = r.json() if "application/json" in ct else r.text
            except Exception:
                body = r.text
            last_err = f"{Fore.RED}Request failed with status code {r.status_code}: {body}{Style.RESET_ALL}"
            break
    raise Exception(last_err or "Request failed with status code 500: Unknown error")
def day(image):
    image = ImageEnhance.Brightness(image).enhance(1.3)
    image = ImageEnhance.Contrast(image).enhance(1.1)
    return image.filter(ImageFilter.GaussianBlur(radius=1))
def night(image):
    image = ImageEnhance.Brightness(image).enhance(0.9)
    image = ImageEnhance.Contrast(image).enhance(1.4)
    return image.filter(ImageFilter.GaussianBlur(radius=0.5))
def main():
    print(f"{Fore.CYAN}Welcome to the Post-Processing Magic Workshop!{Style.RESET_ALL}")
    print(f"{Fore.GREEN}This program generates an image from text and applies post-processing effects.{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Type 'exit' to quit.{Style.RESET_ALL}\n")
    while True:
        user_input = input(f"{Fore.MAGENTA}Enter a description for the image (or 'exit' to quit):\n{Style.RESET_ALL}")
        if user_input.lower() == 'exit':
            print(f"{Fore.RED}Goodbye!{Style.RESET_ALL}")
            break
        try:
            print(f"{Fore.GREEN}\nGenerating image...{Style.RESET_ALL}")
            image = generate_image_from_text(user_input)
            a=input(f"{Fore.BLUE}Do you want to apply post-processing effects? (yes/no): {Style.RESET_ALL}").strip().lower()
            if a != 'yes':
                print(f"{Fore.YELLOW}Skipping post-processing...{Style.RESET_ALL}")
                image.show()
                processed_image = image
            else:
                while True:
                    print (f"{Fore.MAGENTA}Choose a post-processing effect:{Style.RESET_ALL}")
                    print(f"{Fore.CYAN}1. Day{Style.RESET_ALL}")
                    print(f"{Fore.CYAN}2. Night{Style.RESET_ALL}")
                    print(f"{Fore.CYAN}3. exit{Style.RESET_ALL}")
                    choice = input(f"{Fore.BLUE}Enter your choice (1 or 2 or 3): {Style.RESET_ALL}").strip()
                    if choice == "1":
                        processed_image = day(image)
                        processed_image.show()
                        break
                    elif choice == "2":
                        processed_image = night(image)
                        processed_image.show()
                        break
                    elif choice == "3":
                        print(f"{Fore.RED}Exiting post-processing...{Style.RESET_ALL}")
                        processed_image = image
                        processed_image.show()
                        break
                    else:
                        print(f"{Fore.RED}Invalid choice. Applying default post-processing...{Style.RESET_ALL}")
                        processed_image = day(image)
                        processed_image.show()
                        break
            save_option = input(f"{Fore.BLUE}Do you want to save the processed image? (yes/no): {Style.RESET_ALL}").strip().lower()
            if save_option == 'yes':
                file_name = input(f"{Fore.BLUE}Enter a name for the image file (without extension): {Style.RESET_ALL}").strip()
                processed_image.save(f"{file_name}.png")
                print(f"{Fore.GREEN}Image saved as {file_name}.png{Style.RESET_ALL}\n")
            print("-" * 80 + "\n")
        except Exception as e:
            print(f"{Fore.RED}An error occurred: {e}{Style.RESET_ALL}\n")
if __name__ == "__main__":
    main()