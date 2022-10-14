import cv2
import mediapipe as mp
import time

cam = cv2.VideoCapture(0) # start using webcam

# mediapipe functions to detect hands
detHands = mp.solutions.hands
hands = detHands.Hands()
mpDraw = mp.solutions.drawing_utils # mp tool for drawing lines between landmarks

prevTime = 0
currTime = 0

while True:
    item, img = cam.read()
    RGBimg = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) # convert BGR image to RGB format
    results = hands.process(RGBimg) # run mp function to process frame from hands object
    # print(results.multi_hand_landmarks) --- x,y,z coordinates of hand landmarks

    if results.multi_hand_landmarks:
        for mark in results.multi_hand_landmarks: # for each hand detected
            for num, coord in enumerate(mark.landmark): # position data for each landmark
                height, width, c = img.shape # get image size in pixels
                cx, cy = int(coord.x * width), int(coord.y * height) # multiply output (ratio of image pixels) to get position
                print(num, cx, cy) # format: landmark num, x-position, y-position
                if num == 4: # thumb tip landmark
                    cv2.circle(img, (cx, cy), 15, (0, 0, 255), cv2.FILLED) # 

            mpDraw.draw_landmarks(img, mark, detHands.HAND_CONNECTIONS) # draw lines between landmarks

    # get fps
    currTime = time.time()
    fps = 1 / (currTime - prevTime)
    prevTime = currTime

    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                (255, 0, 0), 3)

    cv2.imshow("Image", img)
    cv2.waitKey(1)