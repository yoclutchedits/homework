import cv2
import numpy as np
from tensorflow.keras.models import load_model
model=load_model(
    r"C:\Users\Acer\OneDrive\Attachments\Desktop\python\archive\face_model.h5"#input your fer2013
)
face_cascade=cv2.CascadeClassifier(cv2.data.haarcascades+"haarcascade_frontalface_default.xml")
emotion_labels=['Angry','Disgust','Fear','Happy','Neutral','Sad','Surprise']
cap=cv2.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()
while True:
    ret,frame=cap.read()
    if not ret:
        print("failed to capture image")
        break
    gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    faces=face_cascade.detectMultiScale(gray,scaleFactor=1.1,minNeighbors=5,minSize=(30,30))
    for (x,y,w,h) in faces:
        face=gray[y:y+h,x:x+w]
        face=cv2.resize(face,(48,48))
        face=face/255.0
        face = face.reshape(1, 48, 48,1)
        pred = model.predict(face, verbose=0)
        emotion=emotion_labels[np.argmax(pred)]
        cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
        cv2.putText(frame,emotion,(x,y-10),cv2.FONT_HERSHEY_SIMPLEX,0.9,(0,255,0),2)
    cv2.imshow('emotion detection (press q to quit)',frame)
    if cv2.waitKey(1)&0xFF==ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
