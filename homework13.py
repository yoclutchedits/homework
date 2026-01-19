import cv2
import numpy as np
import matplotlib.pyplot as plt
from colorama import Fore, init
init(autoreset=True)
og = cv2.imread(r'C:\Users\Acer\OneDrive\Attachments\Desktop\python\classwork\example.jpg')
if og is None:
    print(Fore.RED + "Image not found!")
    exit()
rgb = cv2.cvtColor(og, cv2.COLOR_BGR2RGB)
gray = cv2.cvtColor(og, cv2.COLOR_BGR2GRAY)
print(Fore.MAGENTA + 'welcome to photo/video editor ai')
while True:
    print(Fore.MAGENTA + 'select an option:')
    print(Fore.MAGENTA + '1. image editor')
    print(Fore.MAGENTA + '2. video editor')
    print(Fore.MAGENTA + '3. exit')
    choice = input(Fore.MAGENTA + 'enter your choice (1-3): ')
    if choice == '1':
        print(Fore.MAGENTA + 'you selected image editor')
        print(Fore.MAGENTA + '1. color filter application')
        print(Fore.MAGENTA + '2. edge detection and smoothing')
        print(Fore.MAGENTA + '3. crop image')
        print(Fore.MAGENTA + '4. convert to grayscale')
        print(Fore.MAGENTA + '5. rotate image')
        print(Fore.MAGENTA + '6. brightness adjustment')
        print(Fore.MAGENTA + '7. exit to main menu')
        task_choice = input(Fore.MAGENTA + 'enter your choice (1-7): ')
        if task_choice == '1':
            def apply_color_filter(rgb, filtered_type):
                filtered_image = rgb.copy()
                if filtered_type == "red_tint":
                    filtered_image[:, :, 0] = 0
                    filtered_image[:, :, 1] = 0
                elif filtered_type == "green_tint":
                    filtered_image[:, :, 0] = 0
                    filtered_image[:, :, 2] = 0
                elif filtered_type == "blue_tint":
                    filtered_image[:, :, 1] = 0
                    filtered_image[:, :, 2] = 0
                return filtered_image
            filtered_type = None
            while True:
                print(Fore.MAGENTA + 'r: red tint | g: green tint | b: blue tint | s: save | q: quit')
                if filtered_type:
                    filtered_img = apply_color_filter(rgb, filtered_type)
                else:
                    filtered_img = rgb.copy()
                cv2.imshow('filtred images',filtered_img)
                key = cv2.waitKey(0) & 0xFF
                if key == ord('r'):
                    filtered_type = 'red_tint'
                elif key == ord('g'):
                    filtered_type = 'green_tint'
                elif key == ord('b'):
                    filtered_type = 'blue_tint'
                elif key == ord('q'):
                    break
                elif key == ord('s'):
                    save_path = input("Enter filename (.jpg/.png): ").lower()
                    if ".jpg" in save_path or ".png" in save_path:
                        cv2.imwrite(save_path, cv2.cvtColor(filtered_img, cv2.COLOR_RGB2BGR))
                        print(Fore.GREEN + "Saved successfully!")
                    else:
                        print(Fore.RED + "Invalid filename!")
            cv2.destroyAllWindows()
        elif task_choice == '2':
            def display_image(title, img):
                plt.figure(figsize=(10, 7))
                if len(img.shape) == 2:
                    plt.imshow(img, cmap='gray')
                else:
                    plt.imshow(img)
                plt.title(title)
                plt.axis('off')
                plt.show()
            while True:
                print(Fore.MAGENTA + "1.Canny 2.Sobel 3.Laplacian 4.Gaussian 5.Median 6.Exit")
                choice2 = input(Fore.MAGENTA + "enter your choice (1-6): ")
                if choice2 == '1':
                    low = int(input("lower threshold(0-255): "))
                    high = int(input("upper threshold(0-255): "))
                    edges = cv2.Canny(gray, low, high)
                    display_image("Canny", edges)
                    if input("Press 's' to save(press any other key to not save): ").lower() == 's':
                        save_path = input("Enter filename (.jpg/.png): ").lower()
                        cv2.imwrite(save_path, edges)
                elif choice2 == '2':
                    sx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=5)
                    sy = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=5)
                    combined = cv2.bitwise_or(sx.astype(np.uint8), sy.astype(np.uint8))
                    display_image("Sobel", combined)
                    if input("Press 's' to save(press any other key to not save): ").lower() == 's':
                        save_path = input("Enter filename (.jpg/.png): ").lower()
                        cv2.imwrite(save_path, combined)
                elif choice2 == '3':
                    lap = cv2.Laplacian(gray, cv2.CV_64F)
                    lap = np.abs(lap).astype(np.uint8)
                    display_image("Laplacian", lap)
                    if input("Press 's' to save(press any other key to not save): ").lower() == 's':
                        save_path = input("Enter filename (.jpg/.png): ").lower()
                        cv2.imwrite(save_path, lap)
                elif choice2 == '4':
                    k = int(input("kernel size (odd): "))
                    blur = cv2.GaussianBlur(rgb, (k, k), 0)
                    display_image("Gaussian Blur", blur)
                    if input("Press 's' to save(press any other key to not save): ").lower() == 's':
                        save_path = input("Enter filename (.jpg/.png): ").lower()
                        cv2.imwrite(save_path, cv2.cvtColor(blur, cv2.COLOR_RGB2BGR))
                elif choice2 == '5':
                    k = int(input("kernel size (odd): "))
                    median = cv2.medianBlur(rgb, k)
                    display_image("Median Blur", median)
                    if input("Press 's' to save(press any other key to not save): ").lower() == 's':
                        save_path = input("Enter filename (.jpg/.png): ").lower()
                        cv2.imwrite(save_path, cv2.cvtColor(median, cv2.COLOR_RGB2BGR))
                elif choice2 == '6':
                    break

                else:
                    print(Fore.RED + "Invalid choice!")
        elif task_choice == '3':
            crop_img = rgb[50:200, 100:300]
            plt.imshow(crop_img)
            plt.axis('off')
            plt.show()
            if input("Press 's' to save(press any other key to not save): ").lower() == 's':
                save_path = input("Enter filename (.jpg/.png): ").lower()
                cv2.imwrite(save_path, cv2.cvtColor(crop_img, cv2.COLOR_RGB2BGR))
        elif task_choice == '4':
            plt.imshow(gray, cmap='gray')
            plt.axis('off')
            plt.show()
            if input("Press 's' to save(press any other key to not save): ").lower() == 's':
                save_path = input("Enter filename (.jpg/.png): ").lower()
                cv2.imwrite(save_path, gray)
        elif task_choice == '5':
            h, w = rgb.shape[:2]
            M = cv2.getRotationMatrix2D((w//2, h//2), 45, 1)
            rotated = cv2.warpAffine(rgb, M, (w, h))
            plt.imshow(rotated)
            plt.axis('off')
            plt.show()
            if input("Press 's' to save(press any other key to not save): ").lower() == 's':
                save_path = input("Enter filename (.jpg/.png): ").lower()
                cv2.imwrite(save_path, cv2.cvtColor(rotated, cv2.COLOR_RGB2BGR))
        elif task_choice == '6':
            bright = cv2.add(rgb, np.ones(rgb.shape, dtype='uint8') * 50)
            plt.imshow(bright)
            plt.axis('off')
            plt.show()
            if input("Press 's' to save(press any other key to not save): ").lower() == 's':
                save_path = input("Enter filename (.jpg/.png): ").lower()
                cv2.imwrite(save_path, cv2.cvtColor(bright, cv2.COLOR_RGB2BGR))
        elif task_choice == '7':
            continue
        else:
            print(Fore.RED + "Invalid choice!")
    elif choice == '2':
        print(Fore.MAGENTA + 'launching video editor')
        print(Fore.MAGENTA + '1. face detection')
        print(Fore.MAGENTA + '2. face detection with people count')
        video_count = input(Fore.MAGENTA + 'input 1 or 2:')
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print(Fore.RED + 'cannot import camera')
            exit()
        while True:
            ret, frame = cap.read()
            if not ret:
                print(Fore.RED + 'failed to capture image')
                break
            gray_vid = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray_vid, 1.1, 5)
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            if video_count == '2':
                cv2.putText(frame, f'people count: {len(faces)}', (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.imshow('video', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()
    elif choice == '3':
        print(Fore.MAGENTA + 'goodbye')
        break
    else:
        print(Fore.RED + 'invalid choice')
