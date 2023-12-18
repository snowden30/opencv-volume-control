import cv2
import mediapipe as mp
import time

cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

pTime=0
cTime=0

while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    #print(results.multi_hand_landmarks)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):
                # print(id, lm)
                h, w, c = img.shape
                cx, cy = int(lm.x*w), int(lm.y*h)
                print(id, cx, cy)
                if id == 4:
                    cv2.circle(img,(cx,cy),15,(255,0,255),cv2.FILLED)
                    # center then radius then color and then filled to fill the cirlc with that color or else put a integer value for outline

            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)
            # HANDLMS will give the 21 dots and hands.connections will give line connecting them

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_TRIPLEX, 1, (255, 255, 255), 2)
    # puttext helps to overlay text on an image str will be the value then coordinates then font style then size then color and then thickness
    cv2.imshow("Image", img)
    cv2.waitKey(1)
