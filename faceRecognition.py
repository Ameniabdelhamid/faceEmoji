import cv2
import sys
import os
import sqlite3
from cv2 import WINDOW_NORMAL
import subprocess
import numpy as np

#cascPath = sys.argv[1]
cascPath = "C:\\faceMoji\\models\\haarcascade_frontalface_default.xml".format(
    base_path=os.path.abspath(os.path.dirname(__file__)))
faceCascade = cv2.CascadeClassifier(cascPath)
video_capture = cv2.VideoCapture(0)
font = cv2.cv.InitFont(cv2.cv.CV_FONT_HERSHEY_SIMPLEX, 2, 1, 0, 3) #creates a font
def insertOrUpdate(FirstName,LastName,Mood):
    conn=sqlite3.connect("C:\\faceMoji\\MojiBase.db")
    cmd="SELECT * FROM People WHERE  FirstName= '"+str(FirstName)+"'"
    cursor=conn.execute(cmd)
    isRecordExist=0
    for row in cursor:
        isRecordExist=1
    if (isRecordExist==1):
        cmd="UPDATE People SET Mood='"+str(Mood)+" 'WHERE FirstName= '"+str(FirstName)+"'"
    else:
        cmd="INSERT INTO People(FirstName,LastName,Mood) Values( '"+str(FirstName)+"',' "+str(LastName)+"',' "+str(Mood)+"')"
    conn.execute(cmd)
    conn.commit()
    conn.close()
def getProfile(FirstName):
    conn=sqlite3.connect("C:\\faceMoji\\MojiBase.db")
    cmd="SELECT * FROM People WHERE  FirstName= '"+str(FirstName)+"'"
    cursor=conn.execute(cmd)
    profile=None
    for row in cursor:
        profile=row
    conn.close();
    return profile
FirstName=raw_input ('Enter your first name: ')
LastName=raw_input ('Enter your Last name: ')
Mood=raw_input ('Your mood :neutral, anger,disgust,happy, sadness, surprise: ')
insertOrUpdate(FirstName,LastName,Mood)
#sampleNum=0


while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #find faces and return positions of detected faces
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=15,
        minSize=(70, 70),
        flags=cv2.cv.CV_HAAR_SCALE_IMAGE
            )
    cv2.cv
    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
        profile=getProfile(FirstName)
        #print profile
        if(profile!=None):
           cv2.cv.PutText(cv2.cv.fromarray(frame),str(profile[1]), (x,y+h+60),font,255) #draw a text
           cv2.cv.PutText(cv2.cv.fromarray(frame),str(profile[2]), (y,x+h+90),font,255) #draw a text
           cv2.cv.PutText(cv2.cv.fromarray(frame),'Press a to check  mood', (20,50),font,255) #draw a text
          
           
    # Display the resulting frame
    cv2.imshow('Face',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        video_capture.release()
        cv2.destroyAllWindows()
        break
    if cv2.waitKey(1) & 0xFF == ord('a'):
        video_capture.release()
        cv2.destroyAllWindows()
        subprocess.call(" C:/faceMoji/webcam.py ", shell=True)
