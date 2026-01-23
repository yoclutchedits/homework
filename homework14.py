import cv2
import numpy as np
import time
from colorama import Fore, Style , init
init(autoreset=True)
print(Fore.CYAN + 'welcome to the real-time video filter application with face detection!')
face_cascade=cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
def apply_color_filter(image, ft):
    img=image.copy()
    if ft=='red':
        img[:,:,1]=0
        img[:,:,0]=0
    elif ft=='green':
        img[:,:,2]=0
        img[:,:,0]=0
    elif ft=='blue':
        img[:,:,2]=0
        img[:,:,1]=0
    elif ft=='sobel':
        gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        Sobel_x=cv2.Sobel(gray,cv2.CV_64F,1,0,ksize=5)
        Sobel_y=cv2.Sobel(gray,cv2.CV_64F,0,1,ksize=5)
        sob=cv2.bitwise_or(Sobel_x.astype(np.uint8),Sobel_y.astype(np.uint8))
        img=cv2.cvtColor(sob,cv2.COLOR_GRAY2BGR)
    elif ft=='canny':
        gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        can=cv2.Canny(gray,100,200)
        img=cv2.cvtColor(can,cv2.COLOR_GRAY2BGR)
    elif ft=='cartoon':
        gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        gray=cv2.medianBlur(gray,5)
        ct=cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,9,9)
        color=cv2.bilateralFilter(image,9,300,300)
        img=cv2.bitwise_and(color,color,mask=ct)
    elif ft=='laplacian':
        gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        Laplacian=cv2.Laplacian(gray,cv2.CV_64F)
        lap=np.abs(Laplacian).astype(np.uint8)
        img=cv2.cvtColor(lap,cv2.COLOR_GRAY2BGR)
    elif ft == 'gaussian':
        img = cv2.GaussianBlur(image, (7, 7), 0)
    elif ft == 'median':
        img = cv2.medianBlur(image, 7)
    return img
print(Fore.MAGENTA + "press the following keys to change filters:")
print(Fore.CYAN +"n: No filter | r: Red | g: Green | b: Blue | s: Sobel | c: Canny")
print(Fore.CYAN +"o: Cartoon | l: Laplacian | m: Median | a: Gaussian | e: Save | q: Quit")
def main():
    cap=cv2.VideoCapture(0)
    if not cap.isOpened():
        print(Fore.RED + "ERROR: cannot import camera")
        return
    else:
        print(Fore.GREEN + "SUCCESS: camera opened")
    ft='original'
    while True:
        ret,frame=cap.read()
        if not ret:
            print(Fore.RED + "ERROR: failed to capture image")
            break
        gray_face=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        faces=face_cascade.detectMultiScale(gray_face,1.1,5,minSize=(30,30))
        for (x,y,w,h) in faces:
            cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
        out=apply_color_filter(frame,ft)
        cv2.imshow('Filtered Video',out)
        key=cv2.waitKey(1) & 0xFF
        if key==ord('r'):
            ft='red'
            print(Fore.MAGENTA + "Filter changed to RED")
            print(Fore.MAGENTA + "press the following keys to change filters:")
            print(Fore.CYAN +"n: No filter | r: Red | g: Green | b: Blue | s: Sobel | c: Canny")
            print(Fore.CYAN +"o: Cartoon | l: Laplacian | m: Median | a: Gaussian | e: Save | q: Quit")
        elif key==ord('g'):
            ft='green'
            print(Fore.MAGENTA + "Filter changed to GREEN")
            print(Fore.MAGENTA + "press the following keys to change filters:")
            print(Fore.CYAN +"n: No filter | r: Red | g: Green | b: Blue | s: Sobel | c: Canny")
            print(Fore.CYAN +"o: Cartoon | l: Laplacian | m: Median | a: Gaussian | e: Save | q: Quit")
        elif key==ord('b'):
            ft='blue'
            print(Fore.MAGENTA + "Filter changed to BLUE")
            print(Fore.MAGENTA + "press the following keys to change filters:")
            print(Fore.CYAN +"n: No filter | r: Red | g: Green | b: Blue | s: Sobel | c: Canny")
            print(Fore.CYAN +"o: Cartoon | l: Laplacian | m: Median | a: Gaussian | e: Save | q: Quit")
        elif key==ord('s'):
            ft='sobel'
            print(Fore.MAGENTA + "Filter changed to SOBEL")
            print(Fore.MAGENTA + "press the following keys to change filters:")
            print(Fore.CYAN +"n: No filter | r: Red | g: Green | b: Blue | s: Sobel | c: Canny")
            print(Fore.CYAN +"o: Cartoon | l: Laplacian | m: Median | a: Gaussian | e: Save | q: Quit")
        elif key==ord('c'):
            ft='canny'
            print(Fore.MAGENTA + "Filter changed to CANNY")
            print(Fore.MAGENTA + "press the following keys to change filters:")
            print(Fore.CYAN +"n: No filter | r: Red | g: Green | b: Blue | s: Sobel | c: Canny")
            print(Fore.CYAN +"o: Cartoon | l: Laplacian | m: Median | a: Gaussian | e: Save | q: Quit")
        elif key==ord('o'):
            ft='cartoon'
            print(Fore.MAGENTA + "Filter changed to CARTOON")
            print(Fore.MAGENTA + "press the following keys to change filters:")
            print(Fore.CYAN +"n: No filter | r: Red | g: Green | b: Blue | s: Sobel | c: Canny")
            print(Fore.CYAN +"o: Cartoon | l: Laplacian | m: Median | a: Gaussian | e: Save | q: Quit")
        elif key==ord('l'):
            ft='laplacian'
            print(Fore.MAGENTA + "Filter changed to LAPLACIAN")
            print(Fore.MAGENTA + "press the following keys to change filters:")
            print(Fore.CYAN +"n: No filter | r: Red | g: Green | b: Blue | s: Sobel | c: Canny")
            print(Fore.CYAN +"o: Cartoon | l: Laplacian | m: Median | a: Gaussian | e: Save | q: Quit")
        elif key==ord('m'):
            ft='median'
            print(Fore.MAGENTA + "Filter changed to MEDIAN")
            print(Fore.MAGENTA + "press the following keys to change filters:")
            print(Fore.CYAN +"n: No filter | r: Red | g: Green | b: Blue | s: Sobel | c: Canny")
            print(Fore.CYAN +"o: Cartoon | l: Laplacian | m: Median | a: Gaussian | e: Save | q: Quit")
        elif key==ord('a'):
            ft='gaussian'
            print(Fore.MAGENTA + "Filter changed to GAUSSIAN")
            print(Fore.MAGENTA + "press the following keys to change filters:")
            print(Fore.CYAN +"n: No filter | r: Red | g: Green | b: Blue | s: Sobel | c: Canny")
            print(Fore.CYAN +"o: Cartoon | l: Laplacian | m: Median | a: Gaussian | e: Save | q: Quit")
        elif key==ord('n'):
            ft='original'
            print(Fore.MAGENTA + "Filter reset to ORIGINAL")
            print(Fore.MAGENTA + "press the following keys to change filters:")
            print(Fore.CYAN +"n: No filter | r: Red | g: Green | b: Blue | s: Sobel | c: Canny")
            print(Fore.CYAN +"o: Cartoon | l: Laplacian | m: Median | a: Gaussian | e: Save | q: Quit")
        elif key==ord('e'):
            save=input(Fore.CYAN +"Enter filename (.png/.jpg | to save as default enter 'z') enter quit to cancel: ").lower()
            if 'z' in save:
                cv2.imwrite('saved_frame.png', out)
                print(Fore.GREEN + "SUCCESS: Frame saved as saved_frame.png")
            elif save=='quit':
                print(Fore.CYAN + "Save operation cancelled")
            else:
                while True:
                    if '.png' not in save and '.jpg' not in save:
                        print(Fore.RED + "ERROR: invalid file extension")
                        save=input(Fore.CYAN +"Please enter a valid filename (.png/.jpg) enter quit to cancel: ").lower()
                    elif save=='quit':
                        print(Fore.CYAN + "Save operation cancelled")
                        break
                    else:
                        cv2.imwrite(save, out)
                        print(Fore.GREEN + f"SUCCESS: Frame saved as {save}")
                        break
        elif key==ord('q'):
            print(Fore.CYAN + "Exiting program")
            break
    cap.release()
    cv2.destroyAllWindows()
if __name__=='__main__':
    main()
