import cv2
import os
from cvzone.HandTrackingModule import HandDetector
import numpy as np

#variables
width,height=1280,720
folderPath="me/opencv/resources/presentation"
cap=cv2.VideoCapture(0)

#camera setup
cap.set(3,width)
cap.set(4,height)
cap.set(10,100)

#Get the list of presentation images
pathImages=sorted(os.listdir(folderPath),key=len)
print(pathImages)

#Variables
imgNumber=0
hs,ws=int(120*1),int(213*1)
gestureThreshold=500
buttonPressed=False
buttonCounter=0
buttonDelay=10
annotations=[[]]
annotationNumber=-1
annotationStart=False

#hand detector
detector=HandDetector(detectionCon=0.8,maxHands=1)

while True:
    #import images
    success,img=cap.read()
    img=cv2.flip(img,1)
     
    pathFullImage=os.path.join(folderPath,pathImages[imgNumber])
    imgCurrent=cv2.imread(pathFullImage)

    imgResize=cv2.resize(imgCurrent,(ws*4,hs*4))

    hands,img=detector.findHands(img)
    cv2.line(img,(0,gestureThreshold),(width,gestureThreshold),(0,255,0),10)

    if hands and buttonPressed is False:
        hand=hands[0]
        fingers=detector.fingersUp(hand)
        cx,cy=hand['center']
        # print(fingers)
        lmList=hand['lmList']

        #constrain values for easier drawing
        xVal=int (np.interp(lmList[8][0],[width//2,w],[0,width]))
        yVal=int (np.interp(lmList[8][1],[120,height-120],[0,height]))
        indexFinger=xVal,yVal

        if cy<=gestureThreshold: #if hand is at the height of the face
            #gesture 1-left
            if fingers == [1,0,0,0,0]:
                print("Left")
                if imgNumber>0:
                    buttonPressed = True
                    annotations=[[]]
                    annotationNumber=-1
                    annotationStart=False
                    imgNumber -= 1

            #gesture 2-right
            if fingers == [0,0,0,0,1]:
                print("Right")
                if imgNumber < len(pathImages)-1:
                    buttonPressed = True
                    annotations=[[]]
                    annotationNumber=-1
                    annotationStart=False
                    imgNumber += 1

        #gesture 3-show pointer
        if fingers == [0,1,1,0,0]:
            cv2.circle(imgResize,indexFinger,12,(0,0,255),cv2.FILLED)

        #gesture 4-draw pointer
        if fingers == [0,1,0,0,0]:
            if annotationStart is False:
                annotationStart=True
                annotationNumber+=1
                annotations.append([])
            cv2.circle(imgResize,indexFinger,12,(0,0,255),cv2.FILLED)
            annotations[annotationNumber].append(indexFinger)
        else:
            annotationStart =False

        #gesture 5-erase
        if fingers == [0,1,1,1,0]:
            if annotations:
                annotations.pop(-1)
                annotationNumber-=1
                buttonPressed=True
    else:
        annotationStart=False

    #button pressed iterations
    if buttonPressed:
        buttonCounter += 1
        if buttonCounter > buttonDelay:
            buttonCounter = 0
            buttonPressed = False


    for i in range (len(annotations)):
        for j in range(len(annotations[i])):
            if j!=0:
                cv2.line(imgResize,annotations[i][j-1],annotations[i][j],(0,0,200),12)


    # adding webcam on slides
    imgSmall=cv2.resize(img,(ws,hs))
    
    h,w,_=imgResize.shape


    imgResize[0:hs,w-ws:w]=imgSmall

    cv2.imshow("Cam",img)

    cv2.imshow("Slides",imgResize)

    key=cv2.waitKey(1)
    if key ==ord('q'):
        break
