import cv2
import time
import os
import HandTrackingModule as htm
from motormodule import motor

motor2 = motor(2,3,4)
motor1 = motor(17,22,27)
RS=30
LS=25
D= 0.0001
motor1.stop()
motor2.stop()

wCam, hCam = 640, 480

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

folderPath = "/home/pi/Desktop/scratches/Data"
myList = os.listdir(folderPath)
myList.sort()

print(myList)
overlayList = []
for imPath in myList:
    image = cv2.imread(f'{folderPath}/{imPath}')
    #print(f'{folderPath}/{imPath}')
    overlayList.append(image)

#print(len(overlayList))
pTime = 0

detector = htm.handDetector()

tipIds = [4, 8, 12, 16, 20]

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    # print(lmList)

    if len(lmList) != 0:
        fingers = []

        # Thumb
        if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        # 4 Fingers
        for id in range(1, 5):
            if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        # print(fingers)
        totalFingers = fingers.count(1)
        #print(totalFingers)
        
        if totalFingers == 0:
            motor1.moveF(x=RS)
            motor2.moveF(x=LS)
            time.sleep(D)
            

            
            print("Front")   
        elif totalFingers == 5:
            motor1.stop()
            motor2.stop()
         
            print("Stop")
        elif totalFingers == 2:
            motor1.moveB(x=RS)
            motor2.moveB(x=LS)
            time.sleep(D)
            print("Back")
        
        elif totalFingers == 3:
            motor1.moveF(x=RS)
            motor2.moveB(x=LS)
            time.sleep(D)
            print("Back") 
        
        elif totalFingers == 4:
            motor1.moveB(x=RS)
            motor2.moveF(x=LS)
            time.sleep(D)
            print("Back") 
        
        else :
            motor1.stop()
            motor2.stop()
         
            print("Stop")
        h, w, c = overlayList[totalFingers - 1].shape
        img[0:h, 0:w] = overlayList[totalFingers - 1]

        cv2.rectangle(img, (20, 225), (170, 425), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, str(totalFingers), (45, 375), cv2.FONT_HERSHEY_PLAIN,
                    10, (255, 0, 0), 25)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, f'FPS: {int(fps)}', (400, 70), cv2.FONT_HERSHEY_PLAIN,
                3, (255, 0, 0), 3)

    cv2.imshow("Image", img)
    cv2.waitKey(1)
