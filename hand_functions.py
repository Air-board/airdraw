import cv2
import mediapipe as mp


class HandFunctions:

    def __init__(self,mode = False,max_hands = 2,model_complexity = 1,detection_confidence = 0.5,tracking_confidence = 0.5):
        self.mode = mode
        self.max_hands = max_hands
        self.model_complexity = model_complexity
        self.detection_confidence = detection_confidence
        self.tracking_confidence = tracking_confidence

        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(self.mode,self.max_hands,self.model_complexity,self.detection_confidence,
                                         self.tracking_confidence)
        self.fingertip_id = [4,8,12,16,20]

    def find_finger_position(self,img,hand_no = 0):
        img_rgb = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)           # convert cv2 BGR color scheme to RGB for mediapipe
        self.results = self.hands.process(img_rgb)
        self.landmark_list = []
        if self.results.multi_hand_landmarks:
            my_hand = self.results.multi_hand_landmarks[hand_no]
            for id, lm in enumerate(my_hand.landmark):
                height, width, depth = img.shape
                true_x, true_y = int(lm.x * width) , int(lm.y * height)
                self.landmark_list.append([id, true_x, true_y])
        return self.landmark_list

    def fingers_up(self):
        finger_list = []

        if self.landmark_list[self.fingertip_id[0]][1] < self.landmark_list[self.fingertip_id[0]-1][1]:     #thumb check
            finger_list.append(1)
        else:
            finger_list.append(0)

        for id in range(1,5):
            if self.landmark_list[self.fingertip_id[id]][2] < self.landmark_list[self.fingertip_id[id]-2][2]:
                finger_list.append(1)
            else:
                finger_list.append(0)
        return finger_list
