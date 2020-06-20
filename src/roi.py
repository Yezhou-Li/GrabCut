import cv2 as cv
import numpy as np
import datetime as dt 

picPath = '/Users/yezhouli/Desktop/Python/GrabCut/testData/gloves/gloves_3.jpg'
compress = cv.IMREAD_REDUCED_COLOR_2
iter = 1
pic = cv.imread(picPath, compress)
print(pic.shape)

roi = cv.selectROI(windowName="roi", img=pic, showCrosshair=True, fromCenter=False)
print(roi)
cv.destroyAllWindows()

startTime = dt.datetime.now()
mask = np.zeros(pic.shape[:2], np.uint8)
bgdModel = np.zeros((1, 65), np.float64)
fgdModel = np.zeros((1, 65), np.float64)
rect = roi

cv.grabCut(pic, mask, rect, bgdModel, fgdModel, 5, cv.GC_INIT_WITH_RECT)

mask2 = np.where((mask==2)|(mask==0),0,1).astype('uint8')
row, col, channel = pic.shape
for i in range(row):
    for j in range(col):
        if mask2[i, j] == 0:
            for k in range(channel):
                pic[i, j, k] = 255

cv.imshow('processed', pic)

endTime = dt.datetime.now()
span = (endTime-startTime).seconds
print(f'Time: {span}s')

cv.waitKey(0)
cv.destroyAllWindows()

result = pic[ roi[1]:roi[1]+roi[3], roi[0]:roi[2]+roi[0], :]
print(f'Shape of result: {result.shape}')

cv.imwrite('/Users/yezhouli/Desktop/result.jpg', result)

