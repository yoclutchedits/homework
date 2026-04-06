import os
from io import BytesIO
from PIL import Image
import numpy as np
import cv2
from huggingface_hub import InferenceClient
from keys import hf_key
from colorama import Fore, Style, init
init(autoreset=True)
MODELS = ["Qwen/Qwen-Image-Edit", "Qwen/Qwen-Image-Edit-2509", "prithivMLmods/Photo-Restore-i2i"]
def ask_image():
    print(Fore.CYAN + "\n🎯 Pick an image (JPG/PNG/WebP/BMP/TIFF ≤ 8MB) from this folder.")
    while True:
        p = input(Fore.MAGENTA + "Image path: ").strip().strip('"').strip("'")
        if not p or not os.path.isfile(p): 
            print(Fore.RED + "⚠️ Not found.")
            continue
        try: 
            Image.open(p).verify()
        except: 
            print(Fore.RED + "⚠️ Corrupted image.")
            continue
        return p
def impaint(image_path: str, mask_path: str) -> Image.Image:
    img = cv2.imread(image_path, cv2.IMREAD_COLOR)
    if img is None:
        raise Exception("Failed to read image for local inpaint.")
    m = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)
    if m is None:
        raise Exception("Failed to read mask for local inpaint.")
    h, w = img.shape[:2]
    if (m.shape[0], m.shape[1]) != (h, w):
        m = cv2.resize(m, (w, h), interpolation=cv2.INTER_NEAREST)
    _, m_bin = cv2.threshold(m, 10, 255, cv2.THRESH_BINARY)
    out = cv2.inpaint(img, m_bin, inpaintRadius=3, flags=cv2.INPAINT_TELEA)
    out_rgb = cv2.cvtColor(out, cv2.COLOR_BGR2RGB)
    return Image.fromarray(out_rgb)
client = InferenceClient(api_key=hf_key)
def ai(image_path: str, prompt: str) -> Image.Image:
    init_img = Image.open(image_path).convert("RGB")
    buf = BytesIO()
    init_img.save(buf, format="JPEG")
    image_bytes = buf.getvalue()
    print(Fore.CYAN + f"🛰️ Sending to {MODELS[1]}...")
    output_bytes = client.image_to_image(
        image=image_bytes, 
        prompt=prompt,
        model=MODELS[1]
    )
    return Image.open(BytesIO(output_bytes))
def main():
    photo_path = ask_image()
    print(Fore.MAGENTA + "--- Select Mask ---")
    mask_path = ask_image()
    prompt=input("\n🖊️ Describe the restoration task (e.g., 'Remove the white spiderweb scratches and cracks. Do not change the faces.') or press Enter for default: ").strip()
    if not prompt:
        prompt = "Restoration task: Remove the white spiderweb scratches and cracks. Do not change the faces."
    print(Fore.MAGENTA + "\n🔧 Attempting AI restoration...")
    try:
        output_image = ai(photo_path, prompt)
        print(Fore.GREEN + "✅ AI model succeeded.")
        output_image.show()
        if input(Fore.CYAN + "Save AI result? (y/n): ").lower() == 'y':
            output_image.save("ai_restored.jpg")
            print(Fore.GREEN + "✅ Saved as ai_restored.jpg")
    except Exception as e:
        print(Fore.RED + f"⚠️ AI failed: {e}")
        print(Fore.MAGENTA + "🛠️ Falling back to local restoration...")
        try:
            local_result = impaint(photo_path, mask_path)
            print(Fore.GREEN + "✅ Local restoration complete.")
            local_result.show()
            if input(Fore.CYAN + "Save local result? (y/n): ").lower() == 'y':
                local_result.save("local_restored.jpg")
                print(Fore.GREEN + "✅ Saved as local_restored.jpg")
        except Exception as local_e:
            print(Fore.RED + f"❌ Local inpainting also failed: {local_e}")
if __name__ == "__main__":
    main()