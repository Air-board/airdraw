import cv2
import numpy as np
import HandTrackingModule as htm
import CharacterExtraction as chx

cap = cv2.VideoCapture(0)
cap.set(3,640)         # width
cap.set(4,480)          # height

detector = htm.handDetector(detectionCon=0.85)
xp, yp = 0, 0

imgCanvas = np.zeros((480,640,3),np.uint8)

while True:
    success , img = cap.read()
    img = cv2.flip(img,1)       # flip the image to avoid mirror effect

    # Find Hand Landmarks
    img = detector.findHands(img, draw=False)  # draw connection lines between points
    lmlist = detector.findPosition(img, draw=False)  # find coordinates of all the points and paints them if draw
    if len(lmlist) != 0:

        x1, y1 = lmlist[12][1], lmlist[12][2]   # tip of middle
        x2, y2 = lmlist[8][1], lmlist[8][2]   # tip of index

        # Check which fingers are up
        fingers = detector.fingersUp()

        # Drawing Mode
        if fingers[1] and fingers[0]==False and fingers[3]==False and fingers[4]==False:
            cv2.circle(img,(x2,y2),5,(0,0,255),cv2.FILLED)

            if xp == 0 and yp == 0:
                xp, yp = x2, y2

            if fingers[1] and fingers[2]:                                       #erasing
                #cv2.rectangle(img,(x2,y2-20),(x1,y1+20),(0,0,0),cv2.FILLED)
                cv2.line(img, (xp, yp), (x2, y2), (0, 0, 0), 20)
                cv2.line(imgCanvas, (xp, yp), (x2, y2), (0, 0, 0), 20)
                cv2.line(img,(xp,yp),(x1,y1),(0,0,0),20)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), (0, 0, 0), 20)

            else:
                cv2.line(img,(xp,yp),(x2,y2),(0,255,0),2)                       #drawing
                cv2.line(imgCanvas, (xp, yp), (x2, y2), (0, 255, 0), 2)

            xp, yp = x2, y2
        elif fingers[0] and fingers[1] and fingers[2] and fingers[3] and fingers[4]:    #clear screen
            imgCanvas = np.zeros((480, 640, 3), np.uint8)
        elif fingers[4] and fingers[0]==False and fingers[1]==False and fingers[2]==False and fingers[3]==False:
            screenshot = chx.windowImage('Canvas')
            screenshot.clicker()
        else:
            xp ,yp = 0, 0

    imgGray = cv2.cvtColor(imgCanvas,cv2.COLOR_BGR2GRAY)                # Background = black, drawing = white
    _, imgInv = cv2.threshold(imgGray,50,255,cv2.THRESH_BINARY_INV)
    imgInv = cv2.cvtColor(imgInv,cv2.COLOR_GRAY2BGR)                    # Background = white, drawing = black

    img = cv2.bitwise_and(img,imgInv)               # retain original color of the video source
    img = cv2.bitwise_or(img,imgCanvas)             # paste the drawing over the video source

    #img = cv2.addWeighted(img,0.5,imgCanvas,0.5,0)   function to make the drawing in the image but color degradation
    cv2.imshow("Canvas", imgInv)                   # change viewing imgCanvas to imgInv as needed b/w image for screenshot
    cv2.moveWindow("Canvas",0,0)
    cv2.imshow("Video",img)
    cv2.moveWindow("Video",0,0)
    key = cv2.waitKey(1)
    if key%256 == 27:                               # exit when Esc key press
        break