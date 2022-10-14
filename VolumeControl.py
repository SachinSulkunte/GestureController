import cv2
import time
import numpy as np 
import math
from subprocess import call

import HandModule as hm 

#########Params##########
wCam, hCam = 640, 480
#########################

cam = cv2.VideoCapture(0)
cam.set(3, wCam) # prop_id 3 - width, 4 - height
cam.set(4, hCam)

currTime = 0
prevTime = 0

det = hm.handDet()

# applescript parameters
minVol = 0
maxVol = 100
volBar = 400
volume = 0
volPer = 0

while True:
    item, img = cam.read()
    img = det.getHands(img, draw=False)
    landmarks = det.getPosition(img, draw=False)
    if len(landmarks) != 0:
        # print(landmarks[4], landmarks[8])

        tx, ty = landmarks[4][1], landmarks[4][2] # thumb position
        ix, iy = landmarks[8][1], landmarks[8][2] # index position
        cx, cy = (tx + ix) // 2, (ty + iy) // 2    # center point
        
        cv2.circle(img, (tx, ty), 10, (156, 156, 25), cv2.FILLED)
        cv2.circle(img, (ix, iy), 10, (156, 156, 25), cv2.FILLED)
        cv2.line(img, (tx, ty), (ix, iy), (54, 54, 17), 3)
        cv2.circle(img, (cx, cy), 10, (156, 156, 25), cv2.FILLED)

        length = math.hypot(ix - tx, iy - ty)
        # print(length)

        volume = np.interp(length, [25, 200], [minVol, maxVol])
        volBar = np.interp(length, [25, 200], [400, 150])
        volPer = np.interp(length, [25, 200], [0, 100])
        # print(volume)
        command = "osascript -e 'set volume output volume '"
        command = command + str(volume)
        call([command], shell=True) # applescript os call

        if length < 25:
            cv2.circle(img, (cx, cy), 10, (195, 195, 135), cv2.FILLED)

    cv2.rectangle(img, (50, 150), (85, 400), (200, 200, 40), 3)
    cv2.rectangle(img, (50, int(volBar)), (85, 400), (200, 200, 40), cv2.FILLED)
    cv2.putText(img, str(int(volPer)) + "%", (40, 450), cv2.FONT_HERSHEY_PLAIN, 2,
                    (200, 200, 40), 3)

    # get fps
    currTime = time.time()
    fps = 1 / (currTime - prevTime)
    prevTime = currTime

    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                    (0, 0, 255), 3)
    cv2.imshow("Image", img)
    cv2.waitKey(1)