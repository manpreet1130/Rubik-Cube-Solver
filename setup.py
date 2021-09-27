'''
    This file is for setting up the project to be able to work with your lighting conditions. Using the below file will help in masking the colours of the cube.
    The ranges which worked for me were:
    WHITE: 
        lower: [45, 0, 108]
        upper: [179, 70, 255]
    RED:
        lower: [159, 147, 89]
        upper: [179, 255, 255]
    GREEN:
        lower: [45, 86, 70]
        upper: [79, 194, 170]
    YELLOW: 
        lower: [14, 100, 94]
        upper: [50, 255, 255]
    ORANGE:
        lower: [0, 150, 127]
        upper: [11, 255, 255]
    BLUE: 
        lower: [91, 100, 106]
        upper: [117, 230, 209]
'''

import cv2
import numpy as np

'''
    A new window is created which will consist of trackbars which can be used to clearly define the range of the H, S and V for each of the 6 colours
'''

def nothing(): pass

cv2.namedWindow("Trackbar")
cv2.createTrackbar("L-H", "Trackbar", 0, 179, nothing)
cv2.createTrackbar("L-S", "Trackbar", 0, 255, nothing)
cv2.createTrackbar("L-V", "Trackbar", 0, 255, nothing)
cv2.createTrackbar("U-H", "Trackbar", 179, 179, nothing)
cv2.createTrackbar("U-S", "Trackbar", 255, 255, nothing)
cv2.createTrackbar("U-V", "Trackbar", 255, 255, nothing)


cap = cv2.VideoCapture(0)

while True:
    retr, frame = cap.read()
    hsvFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    '''
        Tracker positions are stored into variables using which masks for each colour can be created. This step is to be repeated for each colour and the range of values for each colour is to be stored and used for creating masks.
    '''
    lh = cv2.getTrackbarPos("L-H", "Trackbar")
    ls = cv2.getTrackbarPos("L-S", "Trackbar")
    lv = cv2.getTrackbarPos("L-V", "Trackbar")
    uh = cv2.getTrackbarPos("U-H", "Trackbar")
    us = cv2.getTrackbarPos("U-S", "Trackbar")
    uv = cv2.getTrackbarPos("U-V", "Trackbar")

    lower = np.array([lh, ls, lv])
    upper = np.array([uh, us, uv])
    

    mask = cv2.inRange(hsvFrame, lower, upper)

    cv2.imshow('frame', frame)
    cv2.imshow('mask', mask)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        cap.release()
        break
