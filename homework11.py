import cv2
import matplotlib.pyplot as plt
import numpy as np
def apply_color_filter(image, filtered_type):
    print(f"applying filter: {filtered_type}")
    filtered_image = image.copy()
    if filtered_type == "red_tint":
        filtered_image[:, :, 0] = 0
        filtered_image[:, :, 1] = 0
    elif filtered_type == "green_tint":
        filtered_image[:, :, 0] = 0
        filtered_image[:, :, 2] = 0
    elif filtered_type == "blue_tint":
        filtered_image[:, :, 1] = 0
        filtered_image[:, :, 2] = 0
    elif filtered_type == "increase_red_tint":
        filtered_image[:, :, 2] = cv2.add(filtered_image[:, :, 2], 50)
    elif filtered_type == "decreased_blue_tint":
        filtered_image[:, :, 0] = cv2.subtract(filtered_image[:, :, 0], 50)
    elif filtered_type == "increase_green_tint":
        filtered_image[:, :, 1] = cv2.add(filtered_image[:, :, 1], 50)
    elif filtered_type == "increased_blue_tint":
        filtered_image[:, :, 0] = cv2.add(filtered_image[:, :, 0], 50)
    elif filtered_type == "decreased_green_tint":
        filtered_image[:, :, 1] = cv2.subtract(filtered_image[:, :, 1], 50)
    elif filtered_type == "decreased_red_tint":
        filtered_image[:, :, 2] = cv2.subtract(filtered_image[:, :, 2], 50)
    return filtered_image
image_path = 'example.jpg'
image = cv2.imread(image_path)
if image is None:
    print("Image not found!")
else:
    filtered_type = None
    print('press the following keys to apply filters:')
    print('r: red tint')
    print('g: green tint')
    print('b: blue tint')
    print('i: increase red tint')
    print('d: decrease red tint')
    print('b: increase blue tint')
    print('d: decrease blue tint')
    print('p: increase green tint')
    print('o: decrease green tint')
    print('s: save current filtered image')
    print('q: quit')
    while True:
        if filtered_type:
            filtered_image = apply_color_filter(image, filtered_type)
        else:
            filtered_image = image
        cv2.imshow('filtered image', filtered_image)
        cv2.resizeWindow('filtered image', 600, 600)#the image will be croped you can remoe this line if you want to see the full image
        wait_key = cv2.waitKey(0) & 0xFF
        if wait_key == ord('r'):
            filtered_type = 'red_tint'
        elif wait_key == ord('g'):
            filtered_type = 'green_tint'
        elif wait_key == ord('b'):
            filtered_type = 'blue_tint'
        elif wait_key == ord('i'):
            filtered_type = 'increase_red_tint'
        elif wait_key == ord('o'):
            filtered_type = 'decreased_red_tint'
        elif wait_key == ord('p'):
            filtered_type = 'increase_green_tint'
        elif wait_key == ord('k'):
            filtered_type = 'decreased_green_tint'
        elif wait_key == ord('d'):
            filtered_type = 'decreased_blue_tint'
        elif wait_key == ord('n'):
            filtered_type = 'increased_blue_tint'
        elif wait_key == ord('s'):
            while True:
                save_path = input("Enter the filename to save the filtered image(add .jpg or .png at last): ").lower()
                if ".jpg" in save_path or ".png" in save_path :
                    cv2.imwrite(save_path, filtered_image)
                    print(f"Filtered image saved as {save_path}")
                    break
                else:
                    print("invalid filename. Please try again.")
        elif wait_key == ord('q'):
            print("Exiting...")
            break
        else:
            print("Invalid key pressed. Please try again.")
    cv2.destroyAllWindows()