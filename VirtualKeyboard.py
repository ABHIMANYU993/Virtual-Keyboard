import time
import cv2
import numpy as np
import handdetect as hd
from pynput.keyboard import Controller
import keyboard
import pyautogui

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

text = ""
tx = ""
global ctrl_pressed, shift_pressed
detector = hd.handDetector()

# Keyboard layouts
keys = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P", "DEL"],
        ["A", "S", "D", "F", "G", "H", "J", "K", "L", "ENTER"],
        ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "N2S", "CAP"],
        ["CTRL", "SHIFT", "SPACE"]]
keys1 = [["q", "w", "e", "r", "t", "y", "u", "i", "o", "p", "DEL"],
         ["a", "s", "d", "f", "g", "h", "j", "k", "l", "ENTER"],
         ["z", "x", "c", "v", "b", "n", "m", ",", ".", "N2S", "CAP"],
         ["CTRL", "SHIFT", "SPACE"]]
symbol_keys = [["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "DEL"],
               ["!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "ENTER"],
               ["+", "-", "=", "_", "{", "}", "[", "]", ";", ":", "N2S"],
               ["CTRL", "SHIFT", "SPACE"]]
finalText = ""
keyb = Controller()

# Function to draw the buttons on the image layout
def drawAll(img, buttonList):
    imgNew = np.zeros_like(img, np.uint8)
    for button in buttonList:
        x, y = button.pos
        w, h = button.size
        if button.text == "ENTER":
            # Adjust the 'ENTER' button size to fit the text
            text_size, _ = cv2.getTextSize(button.text, cv2.FONT_HERSHEY_PLAIN, 2.5, 2)
            button.size = [text_size[0], h]
        if button.text == "CAP":
            # Adjust the 'CAP' button size to fit the text
            text_size, _ = cv2.getTextSize(button.text, cv2.FONT_HERSHEY_PLAIN, 2.5, 2)
            button.size = [text_size[0], h]
        if button.text == "DEL":
            # Adjust the 'DEL' button size to fit the text
            text_size, _ = cv2.getTextSize(button.text, cv2.FONT_HERSHEY_PLAIN, 2.8, 2)
            button.size = [text_size[0], h]
        if button.text == "N2S":
            # Adjust the 'N2S' button size to fit the text
            text_size, _ = cv2.getTextSize(button.text, cv2.FONT_HERSHEY_PLAIN, 2.7, 2)
            button.size = [text_size[0], h]
        if button.text == "CTRL":
            # Adjust the 'CTRL' button size to fit the text
            text_size, _ = cv2.getTextSize(button.text, cv2.FONT_HERSHEY_PLAIN, 3, 2)
            button.size = [text_size[0], h]
            # Check if the CTRL is pressed change the colour
            if ctrl_pressed:
                # Draw the 'CTRL' button on the image layout with green
                cv2.rectangle(imgNew, (x, y), (x + button.size[0], y + button.size[1]), (99, 155, 1), cv2.FILLED)
                cv2.putText(imgNew, button.text, (x + 10, y + 65), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)
            else:
                cv2.rectangle(imgNew, (x, y), (x + button.size[0], y + button.size[1]), (96, 96, 96, 127), cv2.FILLED)
                cv2.putText(imgNew, button.text, (x + 10, y + 65), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)
        elif button.text == "SHIFT":
            # Adjust the 'SHIFT' button size to fit the text
            text_size, _ = cv2.getTextSize(button.text, cv2.FONT_HERSHEY_PLAIN, 3, 2)
            button.size = [text_size[0], h]
            # Check if the SHIFT is pressed change the colour
            if shift_pressed:
                # Draw the 'SHIFT' button on the image layout with green
                cv2.rectangle(imgNew, (x + 40, y), (x + button.size[0] + 40, y + button.size[1]), (99, 155, 1),
                              cv2.FILLED)
                cv2.putText(imgNew, button.text, (x + 50, y + 65), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)
            else:
                cv2.rectangle(imgNew, (x + 40, y), (x + button.size[0] + 40, y + button.size[1]), (96, 96, 96, 127),
                              cv2.FILLED)
                cv2.putText(imgNew, button.text, (x + 50, y + 65), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)
        elif button.text == "SPACE":
            # Draw the 'SPACE' button on the image layout after adjusting the size to text
            cv2.rectangle(imgNew, (x + 400, y), (x, y + 95), (96, 96, 96, 127), cv2.FILLED)
            cv2.putText(imgNew, button.text, (x + 115, y + 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 2)
        else:
            # Draw the buttons on the image layout after adjusting the size to text
            cv2.rectangle(imgNew, (x, y), (x + button.size[0], y + button.size[1]), (96, 96, 96, 127), cv2.FILLED)
            cv2.putText(imgNew, button.text, (x + 10, y + 65), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)
    out = img.copy()
    alpha = 0.5
    mask = imgNew.astype(bool)
    out[mask] = cv2.addWeighted(img, alpha, imgNew, 1 - alpha, 0)[mask]
    return out

class Button():
    def __init__(self, pos, text, size):
        self.pos = pos
        self.size = size
        self.text = text

buttonList = []
buttonList1 = []
symbolButtonList = []

for i in range(len(keys)):
    # Encode the buttons on the image layout(Not visilbe)
    for j, key in enumerate(keys[i]):
        if key == "SPACE":
            # Adjust the position of the space button to lower-mid
            buttonList.append(Button([100 * j + 275, 100 * i + 50], key, [400, 85]))
        else:
            buttonList.append(Button([100 * j + 50, 100 * i + 50], key, [85, 85]))
for i in range(len(keys1)):
    for j, key in enumerate(keys1[i]):
        if key == "SPACE":
            buttonList1.append(Button([100 * j + 275, 100 * i + 50], key, [400, 85]))
        else:
            buttonList1.append(Button([100 * j + 50, 100 * i + 50], key, [85, 85]))
for i in range(len(symbol_keys)):
    for j, key in enumerate(symbol_keys[i]):
        if key == "SPACE":
            symbolButtonList.append(Button([100 * j + 275, 100 * i + 50], key, [400, 85]))
        else:
            symbolButtonList.append(Button([100 * j + 50, 100 * i + 50], key, [85, 85]))
app = 0
delay = 0
pTime = 0
cTime = 0
ctrl_pressed = False
shift_pressed = False

while True:
    # Get image frame and flip it
    success, img = cap.read()
    img = cv2.flip(img, 1)
    # Find the hand and its landmarks
    img = detector.findHands(img)
    lmList, bboxInfo = detector.findPosition(img)
    imgNew = np.zeros_like(img, np.uint8)
    if app == 1:
        # Draw the uppercase letters
        img = drawAll(img, buttonList)
        list = buttonList
    if app == 0:
        # Draw the lowercase letters
        img = drawAll(img, buttonList1)
        list = buttonList1
    if app == 2:
        # Draw the numbers and symbolic letters
        img = drawAll(img, symbolButtonList)
        list = symbolButtonList

    if lmList:
        for button in list:
            x, y = button.pos
            w, h = button.size

            # Check if the index finger is over the button
            if x < lmList[8][0] < x + w and y < lmList[8][1] < y + h:
                # Adjust the layout of the 'SPACE' button when the index finger is over the button
                if button.text == "SPACE":
                    cv2.rectangle(img, (x - 0, y - 0), (x + w + 2, y + h + 10), (99, 155, 1), cv2.FILLED)
                    cv2.putText(img, button.text, (x + 115, y + 70),
                                cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 2)
                # Adjust the layout of the 'SHIFT' button when the index finger is over the button
                elif button.text == "SHIFT":
                    cv2.rectangle(img, (x + 35, y - 5), (x + w + 45, y + h + 5), (99, 155, 1), cv2.FILLED)
                    cv2.putText(img, button.text, (x + 50, y + 65),
                                cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)
                else:
                # Adjust the layout of the buttons when the index finger is over the button
                    cv2.rectangle(img, (x - 5, y - 5), (x + w + 5, y + h + 5), (99, 155, 1), cv2.FILLED)
                    cv2.putText(img, button.text, (x + 10, y + 65),
                                cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)

                # Find the distance btw the index and middle finger
                l, _, _ = detector.findDistance(8, 12, img, draw=False)
                if l < 50 and delay == 0:
                    """
                    If the distance btw the index and middle finger is less than 50 pixles
                    press the button on which the index finger is over.
                    To press the same button on the keyboard use the dedicated library
                    to make the task easier.
                    """
                    finalText += button.text
                    k = button.text

                    if k == "SPACE":
                        tx = ' '
                        text += tx
                        keyboard.press(tx)
                        delay = 0.1

                    elif k == "DEL":
                        tx = text[: -1]
                        text = ""
                        text += tx
                        keyboard.press('\b')
                        delay = 0.1

                    elif k == "ENTER":
                        pyautogui.press('enter')
                        delay = 0.1

                    elif k == "CAP":
                        app = 1 - app  # Toggle between uppercase and lowercase layouts
                        delay = 0.1

                    elif k == "N2S":
                        if app == 0 or app == 1:
                            app = 2  # Toggle to N2S keys
                            delay = 0.1
                        else:
                            app = 1
                            delay = 0.1

                    elif k == "CTRL":
                        # Press and hold the 'CTRL' key on the keyboard
                        if ctrl_pressed:
                            pyautogui.keyUp('ctrl')
                            ctrl_pressed = False
                            delay = 0.1
                        else:
                            # Release the 'CTRL' key on the keyboard
                            ctrl_pressed = True
                            pyautogui.keyDown('ctrl')
                            delay = 0.1

                    elif k == "SHIFT":
                        # Press and hold the 'SHIFT' key on the keyboard
                        if shift_pressed:
                            pyautogui.keyUp('shift')
                            shift_pressed = False
                            delay = 0.1
                        else:
                            # Release the 'SHIFT' key on the keyboard
                            shift_pressed = True
                            pyautogui.keyDown('shift')
                            delay = 0.1

                    else:
                        if app == 0:
                            text += k.lower()  # Press lowercase letter on the keyboard
                            keyboard.press(k.lower())
                            delay = 0.1
                        else:
                            text += k  # Press uppercase letter on the keyboard
                            keyb.press(k)
                            delay = 0.1

    # Update the delay on how fast to click the buttons
    if delay != 0:
        delay += 1
        if delay > 4:
            delay = 0
    # Calculate fps
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    # Create a Gray space to display the entered text on the image layout
    cv2.rectangle(img, (90, 610), (1100, 500), (40, 40, 43), cv2.FILLED)

    # Display the entered text on the image layout
    cv2.putText(img, text, (100, 545), cv2.FONT_ITALIC, 1, (255, 255, 255), 2)
    cv2.putText(img, 'Press F2 to end the program', (20, 700), cv2.FONT_ITALIC, 1, (255, 255, 255), 2)

    # If you want to display the fps un-comment the below line

    # cv2.putText(img, str(int(fps)), (10, 35), cv2.FONT_HERSHEY_PLAIN, 2.5,
    #             (255,0,0), 2)

    cv2.imshow("Image", img)

    # Exit the loop on 'F2' key press
    if cv2.waitKey(1) and keyboard.is_pressed("f2"):
        pyautogui.keyUp('ctrl')
        pyautogui.keyUp('shift')
        break
