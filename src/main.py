import numpy as np
import cv2

img = cv2.imread("alliance/hat.JPG")
rows,cols,channels = img.shape
cv2.imshow('girl',img)
 
#转换hsv
hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
cv2.imshow('hsv', hsv)
lower_blue=np.array([0,0,0])
upper_blue=np.array([0,0,255])
mask = cv2.inRange(hsv, lower_blue, upper_blue)
cv2.imshow('Mask', mask)
 
#腐蚀膨胀
erode=cv2.erode(mask,None,iterations=1)
cv2.imshow('erode',erode)
dilate=cv2.dilate(erode,None,iterations=1)
cv2.imshow('dilate',dilate)
 
#遍历替换
for i in range(rows):
    for j in range(cols):
        if dilate[i,j]==255:
            img[i,j]=(0, 255, 0)#此处替换颜色，为BGR通道
cv2.imshow('res',img)
 
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.waitKey(1)