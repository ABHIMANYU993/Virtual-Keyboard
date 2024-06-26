import cv2
import mediapipe as mp
import math


class handDetector():
    """
    Detect Hands using the mediapipe library. Gives the landmarks
    in pixel format. Adds functions like finding how
    many fingers are up or the distance between two fingers. Also
    provides boundary box of the hand found.
    """

    def __init__(self, mode=False, maxHands=2, modelComplexity=1, detectionCon=0.8, trackCon=0.8):
        """
        mode: In static mode, detection is done on each image: slower.
        maxHands: Maximum number of hands to detect.
        detectionCon: Minimum Detection Confidence Threshold.
        trackCon: Minimum Tracking Confidence Threshold.
        """

        self.mode = mode
        self.maxHands = maxHands
        self.modelComplex = modelComplexity
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.modelComplex,
                                        self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils
        self.tipIds = [4, 8, 12, 16, 20]
        self.fingers = []
        self.lmList = []

    def findHands(self, img, draw=True):
        """
        hands in a BGR image.
        img: Image to find the hands in.
        draw: draw the output on the image.
        Image with or without drawings.
        """

        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms,
                                               self.mpHands.HAND_CONNECTIONS)
        return img

    def findPosition(self, img, handnum=0, draw=True):
        """
        landmarks of a single hand and puts them in a list
        in pixel format. Also finds the boundary box around the hand.
        img: main image to find hand in.
        handnum: hand id if more than one hand detected.
        draw: Flag to draw the output on the image.
        returns: list of landmarks in pixel format, bounding box.
        """

        xList = []
        yList = []
        bbox = []
        bboxInf = []
        self.lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handnum]
            for id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape
                px, py = int(lm.x * w), int(lm.y * h)
                xList.append(px)
                yList.append(py)
                self.lmList.append([px, py])
                if draw:
                    cv2.circle(img, (px, py), 5, (255, 0, 255), cv2.FILLED)
            xmin, xmax = min(xList), max(xList)
            ymin, ymax = min(yList), max(yList)
            boxW, boxH = xmax - xmin, ymax - ymin
            bbox = xmin, ymin, boxW, boxH
            cx, cy = bbox[0] + (bbox[2] // 2), \
                     bbox[1] + (bbox[3] // 2)
            bboxInf = {"id": id, "bbox": bbox, "center": (cx, cy)}

            if draw:
                cv2.rectangle(img, (bbox[0] - 20, bbox[1] - 20),
                              (bbox[0] + bbox[2] + 20, bbox[1] + bbox[3] + 20),
                              (0, 255, 0), 2)

        return self.lmList, bboxInf

    def fingersUp(self):
        """
        how many fingers are open and returns in a list.
        Detects left and right hands separately.
        return: List of which fingers are up.
        """

        if self.results.multi_hand_landmarks:
            myHandType = self.handType()
            fingers = []
            # Thumb
            if myHandType == "Right":
                if self.lmList[self.tipIds[0]][0] > self.lmList[self.tipIds[0] - 1][0]:
                    fingers.append(1)
                else:
                    fingers.append(0)
            else:
                if self.lmList[self.tipIds[0]][0] < self.lmList[self.tipIds[0] - 1][0]:
                    fingers.append(1)
                else:
                    fingers.append(0)

            # 4 Fingers
            for id in range(1, 5):
                if self.lmList[self.tipIds[id]][1] < self.lmList[self.tipIds[id] - 2][1]:
                    fingers.append(1)
                else:
                    fingers.append(0)
        return fingers

    def findDistance(self, p1, p2, img, draw=True):
        """
        distance between two landmarks based on their
        index number.
        p1: Point1 - Index of Landmark 1.
        p2: Point2 - Index of Landmark 2.
        img: Image to draw on.
        return: Distance between the required fingers in the form of
        pixels(measure the length of the line drawn btw the fingers).
        """

        if self.results.multi_hand_landmarks:
            x1, y1 = self.lmList[p1][0], self.lmList[p1][1]
            x2, y2 = self.lmList[p2][0], self.lmList[p2][1]
            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

            if draw:
                cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
                cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
                cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
                cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)

            length = math.hypot(x2 - x1, y2 - y1)
            return length, img, [x1, y1, x2, y2, cx, cy]

    def allFingersClosed(self):
        """
        Check if all fingers are closed (all landmarks below certain threshold).
        returns: True if all fingers are open.
        returns: False if all fingers are closed.
        """

        if len(self.lmList) != 0:
            closedFingers = []
            for i in range(5):
                if self.tipIds[i] - 2 >= 0 and self.tipIds[i] < len(self.lmList):
                    if self.lmList[self.tipIds[i]][2] < self.lmList[self.tipIds[i] - 2][2]:
                        closedFingers.append(1)
                    else:
                        closedFingers.append(0)
                else:
                    closedFingers.append(0)
            return all(finger == 1 for finger in closedFingers)
        else:
            return False

    def handType(self):
        """
        Checks if the hand is left or right.
        returns: "Right" or "Left".
        """
        if self.results.multi_hand_landmarks:
            if self.lmList[17][0] < self.lmList[5][0]:
                return "Right"
            else:
                return "Left"


def main():
    cap = cv2.VideoCapture(0)
    detector = handDetector(maxHands=1)
    while True:
        # Get image frame
        success, img = cap.read()
        # Find the hand and its landmarks
        img = detector.findHands(img)
        lmList, bboxInfo = detector.findPosition(img)
        print(detector.handType())

        # Display
        cv2.imshow("Image", img)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()
