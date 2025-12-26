import cv2
h=input("enter the png or jpg image file location:")
image=cv2.imread(h)
while image is None:
    print("Error: unable to load image at",h)
    h=input("Please enter a valid image file location:")
print("image loaded successfully")
resized_image1=cv2.resize(image,(200,200))
resized_image2=cv2.resize(image,(400,400)) 
resized_image3=cv2.resize(image,(600,600))
cv2.imshow('resized image 200x200',resized_image1)
cv2.imshow('resized image 400x400',resized_image2)
cv2.imshow('resized image 600x600',resized_image3)
cv2.waitKey(0)
if cv2.waitKey(0)==ord('s'):
    cv2.imwrite('resized_image1.png',resized_image1)
    cv2.imwrite('resized_image2.png',resized_image2)
    cv2.imwrite('resized_image3.png',resized_image3)
    print("images saved")
else:
    print("images not saved")
cv2.destroyAllWindows()