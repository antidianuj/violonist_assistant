import cv2
import mediapipe as mp
import time
import numpy as np
import math


class posedetect():
    
    def __init__(self, mode=False, smooth=True, detection=0.5, tracking=0.5):
        self.mode=mode
        self.detection=detection
        self.smooth=smooth
        self.tracking=tracking 
        

        self.mpDraw=mp.solutions.drawing_utils
        self.mpPose=mp.solutions.pose
        self.pose=self.mpPose.Pose()
        
        
    def findpose(self,img,draw=True):
        imgRGB=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        self.results=self.pose.process(imgRGB)

        if self.results.pose_landmarks:
            if draw:
               self.mpDraw.draw_landmarks(img,self.results.pose_landmarks,self.mpPose.POSE_CONNECTIONS)
                
        return img
    
    def getpos(self,img,draw=True):
        self.lmlist=[]
        if self.results.pose_landmarks:

            for id,lm in enumerate(self.results.pose_landmarks.landmark):
                h,w,c=img.shape
                p_x=int(lm.x*w)
                p_y=int(lm.y*h)
                
                self.lmlist.append([id,p_x,p_y])
                
                
                if draw:
                    cv2.circle(img,(p_x,p_y),8,(0,255,255),cv2.FILLED)
                    
        
        return img, self.lmlist
    
    def findangle(self,img,p1,p2,p3,draw=True):
        _,x1,y1=self.lmlist[p1]
        _,x2,y2=self.lmlist[p2]
        _,x3,y3=self.lmlist[p3]
        
        angle=math.degrees(math.atan2(y3-y2,x3-x2)-math.atan2(y1-y2,x1-x2))
        
        
        if draw:
            cv2.circle(img,(x1,y1),40,(0,255,0),cv2.FILLED)
            cv2.circle(img,(x2,y2),40,(0,255,0),cv2.FILLED)
            cv2.circle(img,(x3,y3),40,(0,255,0),cv2.FILLED)
            
            cv2.line(img,(x1,y1),(x2,y2),(255,255,0),10)
            cv2.line(img,(x2,y2),(x3,y3),(255,255,0),10)
            
            cv2.putText(img,"Angle: "+str(int(angle))+" Rads",(100,200),cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),3)
        
        return angle
                
            


# def main():
#     cap=cv2.VideoCapture('practice.mp4')
#     detector=posedetect()
#     pres_time=0

#     while True:
#         success,img=cap.read()
#         img=detector.findpose(img)
#         img,lmlist=detector.getpos(img,True)
#         angle_list=[]
        
#         if (len(lmlist)!=0):
#             angle=detector.findangle(img, 12, 14, 16)
#             angle_list.append(angle)
#             percentage=np.interp(angle,(80,200),(0,100))
#             cv2.putText(img,"Curl Level :"+str(int(percentage)),(570,90),cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),3)
#             cv2.rectangle(img,(600,100),(640,150+int(percentage)),(190,190,120),cv2.FILLED)
            
            
#         curr_time=time.time()
#         fps=1/(curr_time-pres_time)
#         pres_time=curr_time
#         cv2.putText(img,"FPS: "+str(int(fps)),(100,100),cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),3)
#         cv2.circle(img,(lmlist[14][1],lmlist[14][2]),20,(255,0,0),cv2.FILLED)
        
        
#         cv2.imshow("Image",img)
        
#         cv2.waitKey(1)
#         # cap.release()
#         # out.release()
#         # cv2.destroyAllWindows()


# if __name__ =="__main__":
#     main()
    