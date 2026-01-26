import mediapipe as mp
import cv2
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    exit()
def get_gesture(hand_landmarks):
    landmarks = hand_landmarks.landmark
    tip_ids = [4, 8, 12, 16, 20]
    pip_ids = [2, 6, 10, 14, 18]
    extended = 0
    for i in range(1, 5):
        if landmarks[tip_ids[i]].y < landmarks[pip_ids[i]].y:
            extended += 1
    if extended == 0 and landmarks[tip_ids[0]].y < landmarks[0].y:
        return "THUMBS UP"
    elif extended >= 4:
        return "OPEN"
    elif extended <= 1:
        return "FIST"
    else:
        return "PARTIAL"
while True:
    success, frame = cap.read()
    if not success:
        break
    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(frame_rgb)
    gesture = 'No hand detected'
    if result.multi_hand_landmarks and result.multi_handedness:
        for hand_landmarks in result.multi_hand_landmarks:
            gesture = get_gesture(hand_landmarks)
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            for tip_id in [4, 8, 12, 16, 20]:
                lm = hand_landmarks.landmark[tip_id]
                x, y = int(lm.x * w), int(lm.y * h)
                cv2.circle(frame, (x, y), 10, (255, 0, 0), cv2.FILLED)
            x_w, y_w = int(hand_landmarks.landmark[0].x * w), int(hand_landmarks.landmark[0].y * h)
            cv2.putText(frame, f'Wrist: ({x_w}, {y_w})', (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    tinted_frame = frame.copy()
    if gesture == "FIST":
        tinted_frame[:, :, 0] = 0 
        tinted_frame[:, :, 1] = 0  
        text_color = (0, 0, 255)   
    elif gesture == "THUMBS UP":
        tinted_frame[:, :, 1] = 0  
        tinted_frame[:, :, 2] = 0  
        text_color = (255, 0, 0)   
    elif gesture == "PARTIAL":
        tinted_frame[:, :, 0] = 0
        tinted_frame[:, :, 2] = 0
        text_color = (0, 255, 0) 
    else:  
        text_color = (255, 255, 255)
    cv2.putText(tinted_frame, f'Gesture: {gesture}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, text_color, 2)
    cv2.imshow("Hand Gesture Recognition", tinted_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
