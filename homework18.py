import cv2
import numpy as np
import mediapipe as mp
import time
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7,min_tracking_confidence=0.5)
filters = ['None', 'gray', 'negative', 'sepia','red', 'green', 'blue','sobel', 'canny', 'cartoon','laplacian', 'median', 'gaussian']
current_filter = 0
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()
last_time = 0
debounce_time = 1 
def apply_filter(frame, filter_name):
    if filter_name == 'None':
        return frame
    elif filter_name == 'gray':
        return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    elif filter_name == 'sepia':
        kernel = np.array([
            [0.272, 0.534, 0.131],
            [0.349, 0.686, 0.168],
            [0.393, 0.769, 0.189]
        ])
        sepia_frame = cv2.transform(frame, kernel)
        sepia_frame = np.clip(sepia_frame, 0, 255)
        return sepia_frame.astype(np.uint8)
    elif filter_name == 'negative':
        return cv2.bitwise_not(frame)
    elif filter_name == 'gaussian':
        return cv2.GaussianBlur(frame, (15, 15), 0)
    elif filter_name == 'median':
        return cv2.medianBlur(frame, 7)
    elif filter_name == 'canny':
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 100, 200)
        return cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
    elif filter_name == 'cartoon':
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.medianBlur(gray, 5)
        edges = cv2.adaptiveThreshold(gray, 255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,9, 9)
        color = cv2.bilateralFilter(frame, 9, 300, 300)
        cartoon = cv2.bitwise_and(color, color, mask=edges)
        return cartoon
    elif filter_name == 'sobel':
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        sobel_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=5)
        sobel_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=5)
        sobel = cv2.magnitude(sobel_x, sobel_y)
        sobel = np.clip(sobel, 0, 255).astype(np.uint8)
        return cv2.cvtColor(sobel, cv2.COLOR_GRAY2BGR)
    elif filter_name == 'laplacian':
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        laplacian = cv2.Laplacian(gray, cv2.CV_64F)
        laplacian = np.clip(np.abs(laplacian), 0, 255).astype(np.uint8)
        return cv2.cvtColor(laplacian, cv2.COLOR_GRAY2BGR)
    elif filter_name == 'red':
        red_frame = frame.copy()
        red_frame[:, :, 0] = 0
        red_frame[:, :, 1] = 0
        return red_frame
    elif filter_name == 'green':
        green_frame = frame.copy()
        green_frame[:, :, 0] = 0
        green_frame[:, :, 2] = 0
        return green_frame
    elif filter_name == 'blue':
        blue_frame = frame.copy()
        blue_frame[:, :, 1] = 0
        blue_frame[:, :, 2] = 0
        return blue_frame
    return frame
while True:
    ret, img = cap.read()
    if not ret:
        print("Can't receive frame")
        break
    img = cv2.flip(img, 1)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
            index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            pinky_tip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]
            middle_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
            ring_tip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP]
            frame_height, frame_width, _ = img.shape
            thumb_x, thumb_y = int(thumb_tip.x * frame_width), int(thumb_tip.y * frame_height)
            index_x, index_y = int(index_tip.x * frame_width), int(index_tip.y * frame_height)
            pinky_x, pinky_y = int(pinky_tip.x * frame_width), int(pinky_tip.y * frame_height)
            middle_x, middle_y = int(middle_tip.x * frame_width), int(middle_tip.y * frame_height)
            ring_x, ring_y = int(ring_tip.x * frame_width), int(ring_tip.y * frame_height)
            cv2.circle(img, (thumb_x, thumb_y), 10, (0, 255, 0), -1)
            cv2.circle(img, (index_x, index_y), 10, (0, 255, 0), -1)
            cv2.circle(img, (pinky_x, pinky_y), 10, (0, 255, 0), -1)
            cv2.circle(img, (middle_x, middle_y), 10, (0, 255, 0), -1)
            cv2.circle(img, (ring_x, ring_y), 10, (0, 255, 0), -1)
            current_time = time.time()
            if abs(thumb_x - index_x) < 30 and abs(thumb_y - index_y) < 30:
                if current_time - last_time > debounce_time:
                    cv2.putText(img, 'picture captured', (10, 30),cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    last_time = current_time
                    cv2.imwrite(f'captured_{int(time.time())}.jpg', img)
                    print("Picture saved")
            elif ((abs(thumb_x - middle_x) < 30 and abs(thumb_y - middle_y) < 30) or(abs(thumb_x - ring_x) < 30 and abs(thumb_y - ring_y) < 30) or(abs(thumb_x - pinky_x) < 30 and abs(thumb_y - pinky_y) < 30)):
                if current_time - last_time > debounce_time:
                    current_filter = (current_filter + 1) % len(filters)
                    last_time = current_time
                    print(f"Switched to filter: {filters[current_filter]}")
    filtered_frame = apply_filter(img, filters[current_filter])
    if filters[current_filter] == 'gray':
        cv2.imshow('gesture controlled photo app',cv2.cvtColor(filtered_frame, cv2.COLOR_GRAY2BGR))
    else:
        cv2.imshow('gesture controlled photo app', filtered_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
