import cv2
import numpy as np
import time

import poseModule as pm

detector=pm.posedetect()

cap=cv2.VideoCapture('practice.mp4')
pres_time=0

while True:
    success,img=cap.read()
    img=detector.findpose(img)
    img,lmlist=detector.getpos(img,True)
    angle_list=[]
    
    if (len(lmlist)!=0):
        angle=detector.findangle(img, 12, 14, 16)
        angle_list.append(angle)
        percentage=np.interp(angle,(80,200),(0,100))
        cv2.putText(img,"Curl Level :"+str(int(percentage)),(570,90),cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),3)
        cv2.rectangle(img,(600,100),(640,150+int(percentage)),(190,190,120),cv2.FILLED)
        
        
    curr_time=time.time()
    fps=1/(curr_time-pres_time)
    pres_time=curr_time
    cv2.putText(img,"FPS: "+str(int(fps)),(100,100),cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),3)
    cv2.circle(img,(lmlist[14][1],lmlist[14][2]),20,(255,0,0),cv2.FILLED)
    
    

    cv2.imshow("Image",img)
    
    cv2.waitKey(1)
    
    