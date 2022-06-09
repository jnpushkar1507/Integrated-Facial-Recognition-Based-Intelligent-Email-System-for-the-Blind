import cv2
import numpy as np
import os
import face_recognition
import pyttsx3
import pyaudio
from time import sleep
engine=pyttsx3.init()


path = 'UserImages'
images = []
classNames = []
myList = os.listdir(path)
for cls in myList:
    curImg = cv2.imread(f'{path}/{cls}')
    images.append(curImg)
    classNames.append(os.path.splitext(cls)[0])

def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

def Login(name):
    if name == 'USER':
        engine.say('Successfully Logged In')
        engine.runAndWait()
        import NewMail.py
        exit(0)
    else:
        engine.say('FACE Id does not matches, cant log you in')
        engine.runAndWait()
        exit(0)


encodeListKnown = findEncodings(images)
print('Encoding completed...')
engine.say('Get Ready For Face Id Verification')
engine.runAndWait()


cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()
    imgS = cv2.resize(img,(0,0),None,0.25,0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS,facesCurFrame)
    
    for encodeFace,faceLoc in zip(encodesCurFrame,facesCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown,encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown,encodeFace)
        matchIndex = np.argmin(faceDis)

        if matches[matchIndex]:
            name = classNames[matchIndex].upper()
            print(name)
            y1,x2,y2,x1 =  faceLoc
            y1,x2,y2,x1 = y1*4,x2*4,y2*4,x1*4  
            cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
            cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)   
            cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
            Login(name)
        
    cv2.imshow('Webcam',img)
    cv2.waitKey(1) 