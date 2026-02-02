import mediapipe as mp
import cv2
import time
import pyautogui
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
import numpy as np
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from math import hypot
import screen_brightness_control as sbc
from colorama import init, Fore, Style
init(autoreset=True)
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils
def volume_and_brightness_control():
    print(f"{Fore.MAGENTA}Starting Hand Gesture Volume, Brightness, and Scroll Control...")
    print(f"{Fore.MAGENTA}Right hand: volume control.")
    print(f"{Fore.MAGENTA}Left hand: brightness control.")
    print(f"{Fore.MAGENTA}Press 'q' to quit.")
    try:
        device = AudioUtilities.GetSpeakers()
        interface = device.Activate(
            IAudioEndpointVolume._iid_, CLSCTX_ALL, None
        )
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        minvol, maxvol, _ = volume.GetVolumeRange()
    except Exception as e:
        print(f"{Fore.RED}Audio control not available:{e}")
        exit()
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print(f"{Fore.RED}Cannot open camera")
        exit()
    while True:
        success, img = cap.read()
        if not success:
            print(f"{Fore.RED}Can't capture frame. Exiting ...")
            break
        img = cv2.flip(img, 1)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(img_rgb)
        if results.multi_hand_landmarks and results.multi_handedness:
            for i, hand_landmarks in enumerate(results.multi_hand_landmarks):
                hand_label = results.multi_handedness[i].classification[0].label
                mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                thumb_tip = hand_landmarks.landmark[ mp_hands.HandLandmark.THUMB_TIP]
                index_tip = hand_landmarks.landmark[ mp_hands.HandLandmark.INDEX_FINGER_TIP]
                h, w, _ = img.shape
                thumb_pos = int(thumb_tip.x * w), int(thumb_tip.y * h)
                index_pos = int(index_tip.x * w), int(index_tip.y * h)
                cv2.circle(img, thumb_pos, 10, (255, 0, 0), cv2.FILLED)
                cv2.circle(img, index_pos, 10, (255, 0, 0), cv2.FILLED)
                cv2.line(img, thumb_pos, index_pos, (255, 0, 0), 3)
                length = hypot(index_pos[0] - thumb_pos[0],index_pos[1] - thumb_pos[1])
                if hand_label == "Right":
                    vol = np.interp(length, [30, 300], [minvol, maxvol])
                    try:
                        volume.SetMasterVolumeLevel(vol, None)
                    except Exception as e:
                        print(f"{Fore.RED}Failed to set volume: {e}")

                    vol_bar = np.interp(length, [30, 300], [400, 150])
                    cv2.rectangle(img, (50, 150), (85, 400), (0, 255, 0), 3)
                    cv2.rectangle(img,(50, int(vol_bar)),(85, 400),(0, 255, 0),cv2.FILLED)
                    cv2.putText(img,f'Vol:{int(np.interp(length, [30, 300], [0, 100]))}%',(40, 450),cv2.FONT_HERSHEY_COMPLEX,1,(0, 255, 0),3)
                elif hand_label == "Left":
                    brightness = np.interp(length, [30, 300], [0, 100])
                    try:
                        sbc.set_brightness(int(brightness))
                    except Exception as e:
                        print(f"{Fore.RED}Failed to set brightness: {e}")
                    bri_bar = np.interp(length, [30, 250], [400, 150])
                    cv2.rectangle(img, (500, 150), (535, 400), (0, 255, 0), 3)
                    cv2.rectangle(img, (500, int(bri_bar)), (535, 400), (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, f'Brightness:{int(brightness)}%', (300, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 3)
        cv2.imshow("Img", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
def scroll():
    import mediapipe as mp
    import cv2
    import time
    import pyautogui
    print(f"{Fore.MAGENTA}Starting Scroll Control...")
    print(f"{Fore.MAGENTA}Show all fingers to scroll up.")
    print(f"{Fore.MAGENTA}Show fist to scroll down.")
    print(f"{Fore.MAGENTA}Press 'q' to quit.")
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(min_detection_confidence=0.7, max_num_hands=1)
    mp_draw = mp.solutions.drawing_utils
    scroll_s = 500
    scroll_d = 0.5
    cam_width, cam_height = 640, 480
    def detect_gesture(landmaks, handness):
        fingers = []
        tips = ( mp_hands.HandLandmark.INDEX_FINGER_DIP, mp_hands.HandLandmark.MIDDLE_FINGER_DIP, mp_hands.HandLandmark.RING_FINGER_DIP, mp_hands.HandLandmark.PINKY_DIP)
        for tip in tips:
            if landmaks.landmark[tip].y < landmaks.landmark[tip - 2].y:
                fingers.append(1)
            else:
                fingers.append(0)
        thumb_tip = landmaks.landmark[mp_hands.HandLandmark.THUMB_TIP]
        thumb_ip = landmaks.landmark[mp_hands.HandLandmark.THUMB_IP]
        if (handness == "Right" and thumb_tip.x > thumb_ip.x) or \
           (handness == "Left" and thumb_tip.x < thumb_ip.x):
            fingers.append(1)
        return "scroll_up" if sum(fingers) == 5 else \
               "scroll_down" if sum(fingers) == 0 else "none"
    cap = cv2.VideoCapture(0)
    cap.set(3, cam_width)
    cap.set(4, cam_height)
    last_scroll = p_time = 0
    while cap.isOpened():
        success, img = cap.read()
        if not success:
            break
        img = cv2.flip(img, 1)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(img_rgb)
        gesture = "none"
        if results.multi_hand_landmarks:
            for hand, handedness_info in zip(results.multi_hand_landmarks,results.multi_handedness):
                handness = handedness_info.classification[0].label
                gesture = detect_gesture(hand, handness)
                mp_draw.draw_landmarks(img, hand, mp_hands.HAND_CONNECTIONS)
                if time.time() - last_scroll > scroll_d:
                    if gesture == "scroll_up":
                        pyautogui.scroll(scroll_s)
                    elif gesture == "scroll_down":
                        pyautogui.scroll(-scroll_s)
                    last_scroll = time.time()
        fps = 1 / (time.time() - p_time) if time.time() != p_time else 0
        p_time = time.time()
        cv2.putText(img, f'FPS:{int(fps)}', (10, 30),cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        cv2.putText(img, f'Gesture:{gesture}', (10, 70),cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        cv2.imshow("Gesture Control", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
print(f'{Fore.MAGENTA}choose function to run:')
print(f'{Fore.MAGENTA}1. Volume Control')
print(f'{Fore.MAGENTA}2. Scroll Control')
print(f'{Fore.MAGENTA}q. Quit')
print(f'{Fore.MAGENTA}enter 1 or 2:')
while True:
    choice = input('enter choice: ').lower()
    if choice == '1':
        volume_and_brightness_control()
    elif choice == '2':
        scroll()
    elif choice == 'q':
        break
    else:
        print(f'{Fore.RED}invalid input')