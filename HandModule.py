import cv2
import mediapipe as mp
import time


class handDet():
    def __init__(self, mode=False, maxHands=2, detConfidence=0.5, trackConfidence=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detConfidence = detConfidence
        self.trackConfidence = trackConfidence

        # mediapipe functions to detect hands
        self.detHands = mp.solutions.hands
        self.hands = self.detHands.Hands()
        self.mpDraw = mp.solutions.drawing_utils

    def getHands(self, img, draw=True):
        RGBimg = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) # convert BGR image to RGB format
        self.results = self.hands.process(RGBimg) # run mp function to process frame from hands object

        if self.results.multi_hand_landmarks:
            for mark in self.results.multi_hand_landmarks: # for each hand detected
                if draw:
                    # draw lines between landmarks
                    self.mpDraw.draw_landmarks(img, mark, self.detHands.HAND_CONNECTIONS)
    
        return img

    def getPosition(self, img, handNum=0, draw=True):
        
        self.coordList = []
        if self.results.multi_hand_landmarks:
            currHand = self.results.multi_hand_landmarks[handNum] # get specific hand data
            
            for id, coord in enumerate(currHand.landmark): # position data for each landmark                
                height, width, c = img.shape # get image size in pixels
                # multiply output (ratio of image pixels) to get position
                cx, cy = int(coord.x * width), int(coord.y * height)
                # print(id, cx, cy) # format: landmark num, x-position, y-position
                self.coordList.append([id, cx, cy])
                if draw:
                    if id == 4: # highlight thumb tip landmark
                        cv2.circle(img, (cx, cy), 10, (131, 131, 0), cv2.FILLED)

        return self.coordList

    def fingers(self):
        results = []
        fingerDict = {'i':[8, 6], 'm':[12, 10], 'r':[16, 14], 'p':[20, 18]} # landmarkers for up/down detection
        for finger in fingerDict:
            upper = fingerDict.get(finger)[0] # higher landmark
            lower = fingerDict.get(finger)[1] # lower landmark
            if self.coordList[upper][2] < self.coordList[lower][2]:    # y-position inverted using OpenCV standards
                results.append(1)
            else:
                results.append(0)
        return results

def main():
    prevTime = 0
    currTime = 0
    cam = cv2.VideoCapture(0) # start using webcam
    det = handDet()

    while True:
        item, img = cam.read()

        img = det.getHands(img)
        coordList = det.getPosition(img)
        if len(coordList) != 0:
            print(coordList)

        # get fps
        currTime = time.time()
        fps = 1 / (currTime - prevTime)
        prevTime = currTime

        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                    (0, 0, 255), 3)

        cv2.imshow("Image", img)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()