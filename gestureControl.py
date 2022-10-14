import cv2
import mediapipe as mp 
import time

import HandModule as hm 

wCam, hCam = 640, 480
cam = cv2.VideoCapture(0)
cam.set(3, wCam)
cam.set(4, hCam)

while True:
    item, img = cam.read()
    cv2.imshow("Stream", img)
    cv2.waitKey(1)