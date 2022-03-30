import cv2
import time
import numpy as np
import HandTrackingModule as htm
import math

wCam , hCam = 640,480

cap = cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)

pTime = 0
cTime = 0

detector = htm.handDetector(detectionCon=0.7)

while True:
    success, img = cap.read()
    img =detector.findHands(img,draw = False)            # draw connection lines between points
    lmlist = detector.findPosition(img,draw = False)     # find coordinates of all the points and paints them if draw
    if len(lmlist) != 0:
        #print(lmlist[4],lmlist[8])

        x1,y1 = lmlist[4][1],lmlist[4][2]
        x2,y2 = lmlist[8][1],lmlist[8][2]
        cx,cy = (x1+x2)//2 , (y1+y2)//2

        cv2.circle(img, (x1, y1), 5, (0, 0, 255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 5, (0, 0, 255), cv2.FILLED)
        cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)
        cv2.circle(img, (cx, cy), 5, (0, 0, 255), cv2.FILLED)

        length = math.hypot(x2-x1,y2-y1)
        print(length)

        if length < 50:
            cv2.circle(img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, f'FPS:{int(fps)}', (10, 40), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 3)
    cv2.imshow("Video",img)
    cv2.waitKey(1)