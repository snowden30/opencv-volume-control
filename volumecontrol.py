import cv2
import time
import numpy as np
import handTrackerModule as htm
import math
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

##
wCam, hCam = 640, 480
##

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0

# creating an object of the ( class hand detector in htm module )
detector = htm.handDetector()

## this is pycaw library of andre miras

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)
# volume.GetMute()
# volume.GetMasterVolumeLevel()
volRange = (volume.GetVolumeRange())

# my audio range is -96 to 0 so -96 means lowest and 0 means full volume
minVol = volRange[0] # so minvol will store -96
maxVol = volRange[1] # and maxvol will store 0
##



while True:
    success, img = cap.read()

    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw = False)
    if len(lmList) !=0:
        # print(lmList[4], lmList[8])  # 4 is for the thumb and 8 is for the index

        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        cx, cy = (x1+x2)//2, (y1+y2)//2

        cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
        cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)

        length = math.hypot(x2-x1, y2-y1)
        #print(length)
        # length range came out between 50 and 300
        # volume range is between -96 and 0
        vol = np.interp(length, [50,300], [minVol, maxVol])
        print(vol)
        volume.SetMasterVolumeLevel(vol, None)  # vol ki jagah 0 tha pehle aur line number 30 par tha

        if length<50:
            cv2.circle(img, (cx, cy), 15, (0, 255, 0), cv2.FILLED)



    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img, f'FPS: {int(fps)}', (40, 50), cv2.FONT_HERSHEY_TRIPLEX, 1, (255, 0, 0), 3)  # it displays fps
    cv2.imshow("Img", img)
    cv2.waitKey(1)  # gives 1 millisecond delay

