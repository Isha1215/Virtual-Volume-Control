import cv2
import mediapipe as mp
import time
import math

class HandDetector():
    def __init__(self,maxHands=2,Trackcon=0.5,DetecCon=0.5,mode=False):
        self.maxHands=maxHands
        self.Trackcon=Trackcon
        self.DetecCon=DetecCon
        self.mode=mode
        self.mp_hands=mp.solutions.hands
        self.hands=self.mp_hands.Hands()
        self.draw=mp.solutions.drawing_utils
    def Hands_draw(self,img,draw=True):
        img_rgb=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        self.results=self.hands.process(img_rgb)
        if self.results.multi_hand_landmarks:
            for handlms in self.results.multi_hand_landmarks:
                if draw:
                    self.draw.draw_landmarks(img,handlms,self.mp_hands.HAND_CONNECTIONS)
    def FindPosition(self,img,draw=True,hand_no=0):
        self.landmarks=[]
        box=[]
        x=[]
        y=[]
        if self.results.multi_hand_landmarks:
            myhand=self.results.multi_hand_landmarks[hand_no]
            for id,lms in enumerate(myhand.landmark):
                h,w,c=img.shape
                cx,cy=int(lms.x*w),int(lms.y*h)
                x.append(cx)
                y.append(cy)
                self.landmarks.append([id,cx,cy])
                if draw:
                    cv2.circle(img,(cx,cy),1,(255,0,255),cv2.FILLED)
            xmin,xmax=min(x),max(x)
            ymin,ymax=min(y),max(y)
            box.append([xmin-20,ymin-20])
            box.append([xmax+20,ymax+20])
            if draw:
                cv2.rectangle(img,box[0],box[1],(0,255,0),2)
        return self.landmarks,box
    def hand_tips(self):
        tips=[4,8,12,16,20]
        finger=[]
        if len(self.landmarks)!=0:
            #Thumb
            if self.landmarks[tips[0]][1]>self.landmarks[tips[0]-1][1]:
                finger.append(1)
            else:
                finger.append(0)
            #Fingers
            for i in range(1,5):
                if self.landmarks[tips[i]][2]<self.landmarks[tips[i] - 2][2]:
                    finger.append(1)
                else:
                    finger.append(0)
        return finger
    def FindDistance(self,p1,p2,img):
        x1, y1=self.landmarks[p1][1:]
        x2, y2 = self.landmarks[p2][1:]
        cx,cy=(x1-x2)//2,(y1-y2)//2
        cv2.line(img,(x1,y1),(x2,y2),(0,0,0),2)
        cv2.circle(img,(x1,y1),10,(0,255,0),cv2.FILLED)
        cv2.circle(img,(x2,y2),10,(0,255,0),cv2.FILLED)
        cv2.circle(img,(x2+cx,y2+cy),10,(255,0,255),cv2.FILLED)
        length=math.hypot(x1-x2,y1-y2)
        return img, [x1,y1,x2,y2,cx,cy], length





