import numpy as np
import cv2
import math
import HandTrackingmodule as htm
import time
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

cap=cv2.VideoCapture(0)
cap.set(3,480)
cap.set(4,640)
detector=htm.HandDetector(DetecCon=0.75)
ptime=0
ctime=0

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
#volume.GetMute()
#volume.GetMasterVolumeLevel()
Volume=volume.GetVolumeRange()
minVol=Volume[0]
maxVol=Volume[1]
Vol_bar=400
Vol_per=0
color=(0,0,0)
curVol=round(volume.GetMasterVolumeLevelScalar()*100)
while True:
    success,img=cap.read()
    detector.Hands_draw(img)
    landmarks,box=detector.FindPosition(img,draw=True)
    ctime=time.time()
    fps=1/(ctime-ptime)
    cv2.putText(img, f'Set Volume: {int(curVol)}', (400, 50), cv2.FONT_HERSHEY_COMPLEX, 0.7, color, 2)
    cv2.putText(img, f'FPS: {int(fps)}', (450, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 2)
    ptime = ctime
    if len(landmarks)!=0:
        img,info,length=detector.FindDistance(4,8,img)
        w,h=box[1][0]-box[0][0],box[1][1]-box[0][1]
        area=int(w*h)//100
        #length(10-250)
        #vol(-65,0)
        #Volume_interpret=np.interp(length,[10,180],[minVol,maxVol])
        if 300<=area<=1500:
            #print("yes")
            smoothnes=5
            Vol_bar=np.interp(length,[20,140],[400,150])
            Vol_per = np.interp(length, [20, 140], [0, 100])
            Vol_per=smoothnes * int(Vol_per/smoothnes)
            #SetMasterVolumeLevelScaler accepts values between 0-1
            fingers=detector.hand_tips()
            print(fingers)
            if fingers[4]==1:
                volume.SetMasterVolumeLevelScalar(Vol_per / 100, None)
                cv2.circle(img,(info[4],info[5]), 10, (0, 255, 0), cv2.FILLED)
                color=(0,255,0)
            else:
                color=(0,0,0)
    curVol = round(volume.GetMasterVolumeLevelScalar() * 100)
    cv2.putText(img, f'FPS: {int(fps)}', (450, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 2)
    cv2.rectangle(img,(30,150),(80,400),(255,0,0),1)
    cv2.rectangle(img, (30, int(Vol_bar)), (80, 400), (255, 0, 0),cv2.FILLED)
    cv2.putText(img,f'{int(Vol_per)}%',(35,450),cv2.FONT_HERSHEY_COMPLEX,1,(255,0,0),2)
        #if length<30:
            #cv2.circle(img, (info[0] + info[4], info[1] + info[5]), 10, (0, 255, 0), cv2.FILLED)
    cv2.imshow("img",img)
    if cv2.waitKey(1) and 0XFF==ord('p'):
        break