import cv2
import numpy as np
import hand_functions as hfx
import character_extraction as chx

capture = cv2.VideoCapture(0)
capture.set(3,640)                                              # width
capture.set(4,480)                                              # height

hand_detector = hfx.HandFunctions(detection_confidence=0.85)
xp, yp = 0, 0

img_canvas = np.zeros((480,640,3),np.uint8)

while True:
    success, img  = capture.read()
    img = cv2.flip(img,1)                                       # flip the image to avoid mirror effect

    landmark_list = hand_detector.find_finger_position(img)
    if len(landmark_list) != 0:

        x1, y1 = landmark_list[12][1], landmark_list[12][2]    # tip of middle
        x2, y2 = landmark_list[8][1], landmark_list[8][2]      # tip of index

        # Check which finger_list are up
        finger_list = hand_detector.fingers_up()

        # Drawing Mode
        if finger_list[1] and finger_list[0] == False and finger_list[3] == False and finger_list[4] == False:
            cv2.circle(img, (x2, y2), 5, (0, 0, 255), cv2.FILLED)

            if xp == 0 and yp == 0:
                xp, yp = x2, y2

            if finger_list[1] and finger_list[2]:                           # erasing index + middle
                cv2.line(img, (xp, yp), (x2, y2), (0, 0, 0), 20)
                cv2.line(img_canvas, (xp, yp), (x2, y2), (0, 0, 0), 20)
                cv2.line(img, (xp, yp), (x1, y1), (0, 0, 0), 20)
                cv2.line(img_canvas, (xp, yp), (x1, y1), (0, 0, 0), 20)

            else:
                cv2.line(img, (xp, yp), (x2, y2), (0, 255, 0), 2)           # drawing index only
                cv2.line(img_canvas, (xp, yp), (x2, y2), (0, 255, 0), 2)

            xp, yp = x2, y2
        elif finger_list[0] and finger_list[1] and finger_list[2] and finger_list[3] and finger_list[4]:  # clear screen all 5 finger_list
            img_canvas = np.zeros((480, 640, 3), np.uint8)
        elif finger_list[4] and finger_list[0] == False and finger_list[1] == False and finger_list[2] == False and finger_list[3] == False:
            screenshot = chx.WindowImage('Canvas')
            screenshot.clicker()
        else:
            xp, yp = 0, 0

    img_gray = cv2.cvtColor(img_canvas, cv2.COLOR_BGR2GRAY)                          # Background = black, drawing = white
    _, img_invert = cv2.threshold(img_gray, 50, 255, cv2.THRESH_BINARY_INV)
    img_invert = cv2.cvtColor(img_invert, cv2.COLOR_GRAY2BGR)                        # Background = white, drawing = black

    img = cv2.bitwise_and(img, img_invert)                              # retain original color of the video source
    img = cv2.bitwise_or(img, img_canvas)                               # paste the drawing over the video source

    cv2.imshow("Canvas", img_invert)             # viewing imgCanvas to imgInv as needed b/w image for screenshot
    cv2.moveWindow("Canvas", 0, 0)
    cv2.imshow("Video", img)
    cv2.moveWindow("Video", 0, 0)
    key = cv2.waitKey(1)
    if key % 256 == 27:  # exit when Esc key press
        break