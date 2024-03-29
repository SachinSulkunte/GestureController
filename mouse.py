import cv2
import mediapipe as mp
import time
import pyautogui
import math
import numpy as np

import HandModule as hm 

# dummy code for implementing module functions
prevTime = 0
currTime = 0

#########Params##########
wCam, hCam = 640, 480
frameReduction = 100
smoothening = 7
#########################

######## Setup ##########
screenWidth, screenHeight = pyautogui.size() # screen size

cam = cv2.VideoCapture(0)
cam.set(3, wCam) # prop_id 3 - width, 4 - height
cam.set(4, hCam)

det = hm.handDet(maxHands=1) # only track one hand for mouse

MOUSE = 0
GESTURE = 1
OFF = 2

click = False

################

mode = MOUSE

while True:
    while mode == MOUSE:
        ret, img = cam.read()

        img = det.getHands(img)
        coords = det.getPosition(img)

        if len(coords) != 0:
            tx, ty = coords[4][1:] # thumb tip position
            ibx, iby = coords[5][1:] # index base position
            ix, iy = coords[8][1:] # index tip position

            fingers = det.fingers() # list of finger states
            if fingers[0] == 1: # index finger up
                # convert coords to screen from cam
                x = np.interp(ix, (0, wCam), (0, screenWidth))
                y = np.interp(iy, (0, hCam), (0, screenHeight))
                if (click == True):
                    cv2.circle(img, (ix, iy), 10, (0, 0, 131), cv2.FILLED) # color click
                    click = False
                else:
                    cv2.circle(img, (ix, iy), 10, (131, 131, 0), cv2.FILLED) # color normal

                pyautogui.moveTo(screenWidth - x, y) # flip movement to undo mirror effect
                # if abs(tx - ix) <= 20: # account for left or right hand usage
                #     print("hand side")
                    # add in code to trace index finger location, smoothen and click 

                if (fingers[0] == 1 and fingers[3] == 1): # click if index + pinky up
                    pyautogui.leftClick()
                    print("click")
                    click = True
                    # cv2.putText(img, str("Click"), (10, 120), cv2.FONT_HERSHEY_PLAIN, 3,
                    # (255, 0, 0), 3)
            
            if ((fingers[0] == 1 and fingers[1] == 1) and (fingers[2] == 0 and fingers[3] == 0)): # index and middle are up
                print("Switching to GESTURE")
                mode = GESTURE
        
        # get fps
        currTime = time.time()
        fps = 1 / (currTime - prevTime)
        prevTime = currTime

        cv2.putText(img, "FPS: " + str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 2,
                    (255, 0, 0), 3)

        cv2.imshow("Image", img)
        cv2.waitKey(1)

    while mode == GESTURE:
        img = det.getHands(img)
        coords = det.getPosition(img)

        if len(coords) != 0:
            tx, ty = coords[4][1:] # thumb tip position
            ibx, iby = coords[5][1:] # index base position
            ix, iy = coords[8][1:] # index tip position

            fingers = det.fingers() # list of finger states
            
            if ((fingers[0] == 1 and fingers[1] == 1) and (fingers[2] == 0 and fingers[3] == 0)): # index and middle are up
                print("Switching to MOUSE")
                mode = MOUSE
                time.sleep(1)
        # TODO: read gesture types and run bash commands/osascript to carry out different functions