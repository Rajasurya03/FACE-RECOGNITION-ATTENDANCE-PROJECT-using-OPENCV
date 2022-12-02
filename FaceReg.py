#Import Modules
import face_recognition as fr
import cv2
import numpy as np
import os
from datetime import datetime as dt

#Image Paths & Name
path='Test'
img=[]
clsName=[]
mylist=os.listdir(path)
print(mylist)

#Image Name -> Name
for cl in mylist:
        curImg=cv2.imread(f'{path}/{cl}')
        img.append(curImg)
        clsName.append(os.path.splitext(cl)[0])
print(clsName)

#Encoding
def en(images):
        encodeList=[]
        for img in images:
                img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
                encode=fr.face_encodings(img)[0]
                encodeList.append(encode)
        return encodeList

encodeListKnown=en(img)
print('Encoding Completed ...✌')

#Excel Sheet
def mrkAtt(name):
        with open('Note.csv','r+') as f:
                myDataList=f.readlines()
                nameList=[]
                for line in myDataList:
                        entry=line.split(',')
                        nameList.append(entry[0])
                if name not in nameList:
                        now=dt.now()
                        dtString=now.strftime('%H:%M:%S')
                        f.writelines(f'\n{name},{dtString}')

cap=cv2.VideoCapture(0)

while True:
        success, img=cap.read()
        imgrz=cv2.resize(img,(0,0),None,0.25,0.25)
        imgrz=cv2.cvtColor(imgrz,cv2.COLOR_BGR2RGB)

        facesCurFrame=fr.face_locations(imgrz)
        encodeCurFrame=fr.face_encodings(imgrz,facesCurFrame)

        for encodeFace, faceLoc in zip(encodeCurFrame,facesCurFrame):
                matches=fr.compare_faces(encodeListKnown,encodeFace)
                faceDis=fr.face_distance(encodeListKnown,encodeFace)
                print(faceDis)
                matchIndex=np.argmin(faceDis)

                if matches[matchIndex]:
                        name=clsName[matchIndex].upper()
                        print(name)
                        y1, x2, y2, x1=faceLoc
                        y1, x2, y2, x1=y1*4, x2*4, y2*4, x1*4
                        cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
                        cv2.rectangle(img,(x1,y2-35),(x2,y2),(255,0,0),cv2.FILLED)
                        cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
                        mrkAtt(name)
                        
                else:
                        y1, x2, y2, x1=faceLoc
                        y1, x2, y2, x1=y1*4, x2*4, y2*4, x1*4
                        cv2.circle(img,(x1+60,y1+60),115,(255,0,0),2)
                        cv2.rectangle(img,(x1,y2+60),(x2,y2),(0,0,255),cv2.FILLED)
                        cv2.putText(img,"Unknown",(x1+6,y2+30),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)


        cv2.imshow('Webcam',img)
        cv2.waitKey(1)
