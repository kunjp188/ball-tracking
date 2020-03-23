import numpy as np
import cv2

lowerBound00 = (2,110,130)
upperBound00 = (7,250,210)

lowerBound01 = (1,1,1)
upperBound01 = (0,0,0)

lowerBound02 = (2,125,95)
upperBound02 = (7,250,240)


lowerBound10 = (2,100,125)
upperBound10 = (9,235,220)

lowerBound11 = (0,65,135)
upperBound11 = (9,235,230)

lowerBound12 = (2,105,95)
upperBound12 = (7,250,220)


lowerBound20 = (2,155,125)
upperBound20 = (7,250,220)

lowerBound21 = (2,125,120)
upperBound21 = (7,255,240)

lowerBound22 = (2,145,85)
upperBound22 = (7,255,200)


lowerBound30 = (2,160,115)
upperBound30 = (9,255,190)

lowerBound31 = (2,80,100)
upperBound31 = (7,250,210)

lowerBound32 = (2,125,70)
upperBound32 = (7,250,225)


lowerBound40 = (2,145,85)
upperBound40 = (7,255,195)

lowerBound41 = (2,120,115)
upperBound41 = (7,250,215)

lowerBound42 = (1,1,1)
upperBound42 = (0,0,0)


lowerBound50 = (1,1,1)
upperBound50 = (0,0,0)

lowerBound51 = (2,160,65)
upperBound51 = (7,255,205)

lowerBound52 = (1,1,1)
upperBound52 = (0,0,0)

def filter_color(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	
    frame00 = hsv[0:69, 0:426]
    frame01 = hsv[0:69, 426:853]
    frame02 = hsv[0:69, 853:1280]
    frame10 = hsv[69:137, 0:426]
    frame11 = hsv[69:137, 426:853]
    frame12 = hsv[69:137, 853:1280]
    frame20 = hsv[137:206, 0:426]
    frame21 = hsv[137:206, 426:853]
    frame22 = hsv[137:206, 853:1280]
    frame30 = hsv[206:275, 0:426]
    frame31 = hsv[206:275, 426:853]
    frame32 = hsv[206:275, 853:1280]
    frame40 = hsv[275:343, 0:426]
    frame41 = hsv[275:343, 426:853]
    frame42 = hsv[275:343, 853:1280]
    frame50 = hsv[343:412, 0:426]
    frame51 = hsv[343:412, 426:853]
    frame52 = hsv[343:412, 853:1280]

    colorMask00 = cv2.inRange(frame00, lowerBound00, upperBound00)
    colorMask01 = cv2.inRange(frame01, lowerBound01, upperBound01)
    colorMask02 = cv2.inRange(frame02, lowerBound02, upperBound02)
    colorMask10 = cv2.inRange(frame10, lowerBound10, upperBound10)
    colorMask11 = cv2.inRange(frame11, lowerBound11, upperBound11)
    colorMask12 = cv2.inRange(frame12, lowerBound12, upperBound12)
    colorMask20 = cv2.inRange(frame20, lowerBound20, upperBound20)
    colorMask21 = cv2.inRange(frame21, lowerBound21, upperBound21)
    colorMask22 = cv2.inRange(frame22, lowerBound22, upperBound22)
    colorMask30 = cv2.inRange(frame30, lowerBound30, upperBound30)
    colorMask31 = cv2.inRange(frame31, lowerBound31, upperBound31)
    colorMask32 = cv2.inRange(frame32, lowerBound32, upperBound32)
    colorMask40 = cv2.inRange(frame40, lowerBound40, upperBound40)
    colorMask41 = cv2.inRange(frame41, lowerBound41, upperBound41)
    colorMask42 = cv2.inRange(frame42, lowerBound42, upperBound42)
    colorMask50 = cv2.inRange(frame50, lowerBound50, upperBound50)
    colorMask51 = cv2.inRange(frame51, lowerBound51, upperBound51)
    colorMask52 = cv2.inRange(frame52, lowerBound52, upperBound52)

    leftMiddle0 = np.concatenate((colorMask00, colorMask01), axis=1)
    leftMiddle1 = np.concatenate((colorMask10, colorMask11), axis=1)
    leftMiddle2 = np.concatenate((colorMask20, colorMask21), axis=1)
    leftMiddle3 = np.concatenate((colorMask30, colorMask31), axis=1)
    leftMiddle4 = np.concatenate((colorMask40, colorMask41), axis=1)
    leftMiddle5 = np.concatenate((colorMask50, colorMask51), axis=1)

    row0 = np.concatenate((leftMiddle0, colorMask02), axis=1)
    row1 = np.concatenate((leftMiddle1, colorMask12), axis=1)
    row2 = np.concatenate((leftMiddle2, colorMask22), axis=1)
    row3 = np.concatenate((leftMiddle3, colorMask32), axis=1)
    row4 = np.concatenate((leftMiddle4, colorMask42), axis=1)
    row5 = np.concatenate((leftMiddle5, colorMask52), axis=1)

    row01 = np.concatenate((row0, row1), axis=0)
    row23 = np.concatenate((row2, row3), axis=0)
    row45 = np.concatenate((row4, row5), axis=0)

    row0123 = np.concatenate((row01, row23), axis=0)

    combined = np.concatenate((row0123, row45), axis=0)
    return combined