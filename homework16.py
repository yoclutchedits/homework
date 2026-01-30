from ctypes import cast, POINTER
import cv2
from comtypes import CLSCTX_ALL
import mediapipe as mp
import numpy as np
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from math import hypot
import screen_brightness_control as sbc
from colorama import init, Fore, Style
init(autoreset=True)
print(f"{Fore.MAGENTA}Starting Hand Gesture Volume and Brightness Control...")
print(f"{Fore.MAGENTA}right hand: volume control.")
print(f"{Fore.MAGENTA}left hand: brightness control.")
print(f"{Fore.MAGENTA}Press 'q' to quit.")
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils
try:
    device = AudioUtilities.GetSpeakers()
    interface = device.Activate(IAudioEndpointVolume._iid_,CLSCTX_ALL,None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    minvol, maxvol, _ = volume.GetVolumeRange()
except Exception as e:
    print(f"{Fore.RED}Audio control not available: {e}")
    exit()
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print(f"{Fore.RED}Cannot open camera")
    exit()
else:
    print(f"{Fore.GREEN}Camera successfully opened.")
while True:
    success, img = cap.read()
    if not success:
        print(f"{Fore.RED}Can't capture frame. Exiting ...")
        break
    img=cv2.flip(img,1)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)
    if results.multi_hand_landmarks and results.multi_handedness:
        for i, hand_landmarks in enumerate(results.multi_hand_landmarks):
            hand = results.multi_handedness[i].classification[0].label
            mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
            index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            h, w, _= img.shape
            thumb_pos = int(thumb_tip.x * w), int(thumb_tip.y * h)
            index_pos = int(index_tip.x * w), int(index_tip.y * h)
            cv2.circle(img, thumb_pos, 10, (255, 0, 0), cv2.FILLED)
            cv2.circle(img, index_pos, 10, (255, 0, 0), cv2.FILLED)
            cv2.line(img, thumb_pos, index_pos, (255, 0, 0), 3)
            length = hypot(index_pos[0] - thumb_pos[0], index_pos[1] - thumb_pos[1])
            if hand == "Right":
                vol = np.interp(length, [30, 250], [minvol, maxvol])
                try:
                    volume.SetMasterVolumeLevel(vol, None)
                except Exception as e:
                    print(f"{Fore.RED}Failed to set volume: {e}")
                vol_bar= np.interp(length, [30, 250], [400, 150])
                cv2.rectangle(img, (50, 150), (85, 400), (0, 255, 0), 3)
                cv2.rectangle(img, (50, int(vol_bar)), (85, 400), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, f'Vol:{int(np.interp(length, [30, 250], [0,100]))}%', (40, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 3)
            elif hand == "Left":
                brightness = np.interp(length, [30, 250], [0, 100])
                try:
                    sbc.set_brightness(int(brightness))
                except Exception as e:
                    print(f"{Fore.RED}Failed to set brightness: {e}")
                bri_bar = np.interp(length, [30, 250], [400, 150])
                cv2.rectangle(img, (500, 150), (535, 400), (0, 255, 0), 3)
                cv2.rectangle(img, (500, int(bri_bar)), (535, 400), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, f'Brightness:{int(brightness)}%', (300, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 3)
            if hand=="Right":
                cv2.putText(img, f'Hand: {hand} (Volume Control)', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            elif hand=="Left":
                cv2.putText(img, f'Hand: {hand} (Brightness Control)', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    else:
        cv2.putText(img, 'No hands detected', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    cv2.imshow("gesture control", img)
    if cv2.waitKey(1)&0xFF==ord('q'):
        print(f"{Fore.RED}Exiting...")
        break
print(f"{Fore.GREEN}thanks for using Hand Gesture Volume and Brightness Control!")
print(f"{Fore.GREEN}Goodbye!")
cap.release()
cv2.destroyAllWindows()